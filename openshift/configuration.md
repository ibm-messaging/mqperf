## OpenShift Configuration
This document contains guidance on setting up an MQ QM (as part of CP4I) and running an MQ workload against the QM. 
The relevant yaml that was used in the configuration will be provided and any limitations (and workarounds) will be documented to define
the environment used for the openshift performance whitepapers.

### Rebuilding MQ CP4I Image
The [repository](https://github.com/ibm-messaging/mq-container) that controls the creation of the MQ image has been rebuilt with the following changes:
* qmgr.go edited to support fastpath bindings, unlimited channels and 4GB log fileset
* disable.mqsc added to disable channelauth and create the required queues

The integration (CP4I) MQ image has then been rebuilt to use the rebuilt MQ image above.

The initial set of tests will be conducted with both the MQ client and MQ QM located in the same cluster and using a private network, and thus TLS communication is not required. Further tests will be completed with the MQ client outside of the cluster, with and without TLS enabled.

These steps should not be required when the capability to configure these parameters is enabled in the MQ deployment mechanism.

### MQ client deployment
Details of building and deploying the CPH client on OCP are provided in the cphtestp repository [instructions](https://github.com/ibm-messaging/cphtestp/blob/master/openshift/openshift.md). The majority of our testing is performed with the CPH client, but we also have instructions on setting up a JMS client for use with OCP in the jmstestp repository [instructions](https://github.com/ibm-messaging/jmstestp/blob/master/openshift.md).

### Additional network configuration
The default SDN (Software Defined Network) for our OCP 4.2 cluster uses 1Gb networking for all its communication between master->workers as well as workers->workers and external clients->workers. This obviously creates a network bottleneck when testing high throughput messaging. We have a 10GbE network  available across our cluster and clients, so we need to take advantage of this. This can be achieved using the Multus CNI plugin.

At OCP 4.2.x, although the documentation suggests adding additional host networks is straightforward, it appears that further Multus interoperation will only be available in OCP 4.4.x, and that will only be at 'Tech Preview' level of support. There is some base functionality (even at 4.2), that is usable and is available by configuring the network.operator.openshift.io custom resource (CR) which stores the settings for the Cluster Network Operator (CNO). Occasionally it will serve up IP addresses that have already been allocated, and thus attempts to connect to the QM will fail.
```
oc edit networks.operator.openshift.io cluster
```
and you will need to add an entry similar to the following
```
  additionalNetworks:
  - name: tengig
    namespace: mqns
    rawCNIConfig: '{
      "cniVersion": "0.3.1",
      "name": "eth1",
      "type": "host-device",
      "pciBusID": "0000:06:00.0",
      "ipam": {
        "type": "host-local",
        "ranges": [
          [ {
            "subnet": "172.xx.yy.0/24",
            "rangeStart": "172.xx.yy.64",
            "rangeEnd": "172.xx.yy.70"
          } ]
        ]
      }
    }'
    type: Raw
```
The interesting parts of the above configuration are the PCI Bus location of the additional network card that you wish to use, and then the network range from which you would like IP addresses assigned as pods are created and connected to the additional network.

The stateful set yaml that controls the QM deployment will also need to refer to the additional network:
```
     annotations:
        k8s.v1.cni.cncf.io/networks: mqns/tengig
```
and you can see how its referenced by our MQ client application in our sample [cphtestp-job.yaml](https://github.com/ibm-messaging/cphtestp/blob/master/openshift/cphtestp-job.yaml) that you can find in the cphtestp repository.

### Increasing the pid limit
The default value for pids_limit in the CRI-O environment which OpenShift 4 now supports is 1024 user processes. 
This has been reduced from the default 4096 found in docker runtime environments. Whilst this is adequate for the vast majority of scenarios, there may be cases where this proves a limitation. 

A straightfoward approach wasnt initially found, and I described a workaround [here](./pidlimit-old.md). Its now been revealed that there is a more sensible method for effecting the change to the crio configuration, and thats using a ContainerRuntimeConfig:
```
apiVersion: machineconfiguration.openshift.io/v1
kind: ContainerRuntimeConfig
metadata:
  name: set-pid-4k
spec:
  machineConfigPoolSelector:
    matchLabels:
      config-crio: set-pid
  containerRuntimeConfig:
    pidsLimit: 4096
```
Once this resource has been created, edit the mcp/worker yaml to apply the configuration, by specifying the matching label:
```
  labels:
    config-crio: set-pid
```

An update to the OpenShift documentation to communicate this mechanism will made in a future release. There has been a relevant blog discussion on the subject [here](https://www.redhat.com/en/blog/red-hat-openshift-container-platform-4-now-defaults-cri-o-underlying-container-engine)
