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
Details of building and deploying the CPH client on OCP are provided in the cphtestp repository [instructions](https://github.com/ibm-messaging/cphtestp/blob/master/openshift/openshift.md). The majority of our testing is performed with the CPH client, but we also have instructions on setting up a JMS client for use with OCP in the jmstestp repository [instructions](https://github.com/ibm-messaging/jmstestp/blob/master/openshift.md)

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
This has been reduced from the default 4096 found in docker runtime environments. Whilst this is adequate for the vast majority of scenarios, there may be cases where this proves a limitation. It seems there isnt a straightforward approach to reconfiguring this value to support more threads. I initially tried to configure podPidsLimit in the same way as configuring maxPods, by the application of a KubletConfiguration:
```
apiVersion: machineconfiguration.openshift.io/v1
kind: KubeletConfig
metadata:
  name: set-max-pids 
spec:
  machineConfigPoolSelector:
    matchLabels:
      custom-kubelet: pids-4K 
  kubeletConfig:
    maxPods: 500
    podPidsLimit: 4096 
 ```
whilst this seems to work, and the configuration is applied to the node. The Pods deployed subsequently are still limited.
 
The way to increase the pid limit is via the /etc/crio/crio.conf file deployed on each worker node. There is a mechanism where you can base64 encode the entire crio.conf file and overwrite the existing file as part of a [MachineConfig](https://github.com/openshift/machine-config-operator), but this appears clumsy and isnt future proof as will override any subsequent changes to crio.conf. Ive raised the following [bugzilla](https://bugzilla.redhat.com/show_bug.cgi?id=1844447) on this issue. In the meantime, Ive adopted the following to enable large numbers of threads to be used by both my client application and the QM.

Select a worker node to deploy your client onto, ssh onto the worker node(you will need access to the bastion node) and manually change the pids_limit setting in crio.conf to a larger value. Whilst you are logged onto the worker node, restart the crio service 'sudo systemctl restart crio'. You will then need to modify your job/pod yaml to ensure that node is chosen.

```
      nodeSelector: 
        kubernetes.io/hostname : <worker1.hostname.com>
```

A similar approach can be taken for editing the crio.conf on the Node the QM is running on. After restarting the crio service, update the MQ QM stateful set yaml to use a nodeSelector to pin the QM to a particular node and delete the pod to trigger its recreation. 
