## OpenShift Configuration
This document contains guidance on setting up an MQ QM (as part of CP4I) and running an MQ workload against the QM. 
The relevant yaml that was used in the configuration will be provided and any limitations (and workarounds) will be documented to define
the environment used for the openshift performance whitepapers.

### Rebuilding MQ CP4I Image
These steps are no longer required, now that these configuration changes can be made using ConfigMaps in conjunction with QM yaml and the MQ Operator. At this moment its still not possible to alter the size of the MQ log extents (defaults to 16MB), so 64 Primary log files are used to produce a total of 1GB log files.

The [repository](https://github.com/ibm-messaging/mq-container) that controls the creation of the MQ image has been rebuilt with the following changes:
* qmgr.go edited to support fastpath bindings, unlimited channels and 4GB log fileset
* disable.mqsc added to disable channelauth and create the required queues

The integration (CP4I) MQ image has then been rebuilt to use the rebuilt MQ image above.

The initial set of tests will be conducted with both the MQ client and MQ QM located in the same cluster and using a private network, and thus TLS communication is not required. Further tests will be completed with the MQ client outside of the cluster, with and without TLS enabled.


### MQ client deployment
Details of building and deploying the CPH client on OCP are provided in the cphtestp repository [instructions](https://github.com/ibm-messaging/cphtestp/blob/master/openshift/openshift.md). The majority of our testing is performed with the CPH client, but we also have instructions on setting up a JMS client for use with OCP in the jmstestp repository [instructions](https://github.com/ibm-messaging/jmstestp/blob/master/openshift.md).

### Additional network configuration
The default SDN (Software Defined Network) for our OCP 4.2 cluster uses 1Gb networking for all its communication between master->workers as well as workers->workers and external clients->workers. This obviously creates a network bottleneck when testing high throughput messaging. We have a 10GbE and 100GbE network available across our cluster and clients, so we need to take advantage of this. This can be achieved using the Multus CNI plugin.

At OCP 4.2.x, although the documentation suggests adding additional host networks is straightforward, it appears that further Multus interoperation will only be available in OCP 4.4.x, and that will only be at 'Tech Preview' level of support. There is some base functionality (even at 4.2), that is usable and is available by configuring the network.operator.openshift.io custom resource (CR) which stores the settings for the Cluster Network Operator (CNO). Occasionally it will serve up IP addresses that have already been allocated, and thus attempts to connect to the QM will fail.
```
oc edit networks.operator.openshift.io cluster
```
and you will need to add an entry similar to the following
```
  additionalNetworks:
  - name: tengig
    namespace: default
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
        k8s.v1.cni.cncf.io/networks: default/tengig
```
and you can see how its referenced by our MQ client application in our sample [cphtestp-job.yaml](https://github.com/ibm-messaging/cphtestp/blob/master/openshift/cphtestp-job.yaml) that you can find in the cphtestp repository.

You can view the additional networks by:
```
oc get network-attachment-definitions -n default
NAME     AGE
tengig   49m
```

If you define your additional network within a particular namespace, it can only be accessed from within that namespace. You can use the default namespace (or global namespaces config) if you wish to share it across multiple namespaces. Different configurations (in different namespaces) applied to network interfaces on the same switch/routing can communicate with each other, but for ease of management (of resources and IP addresses), its best to stick to a single namespace.

#### Whereabouts
There is now a better CNI IPAM plugin called whereabouts that stores IP addresses in a cluster wide config to avoid reissuing the same IPs to Pod across the cluster, so Ive now updated the config to:
```
  additionalNetworks:
  - name: tengig
    namespace: default
    rawCNIConfig: '{
      "cniVersion": "0.3.1",
      "name": "eth1",
      "type": "host-device",
      "pciBusID": "0000:06:00.0",
      "ipam": {
        "type": "whereabouts",
        "range": "10.20.37.0/24", 
        "exclude": [ 
               "10.20.37.0/27"
            ]
      }
    }'
    type: Raw
```
As before, setting this in the cluster network configuration, automatically generates the NetworkAttachmentDefinition:
```
oc get net-attach-def -n default
NAME            AGE
tengig          6d
```

With this working well, and due to the use of host-device CNI type, those IP addresses are contactable from outside the cluster. You must ensure that the declared range includes the network gateway address (10.20.37.0 in this case); and I used exclude to force IP addresses to start from 10.20.37.32.

#### 100GbE
Now wanting to run NativeHA (which replicates MQ log data from the Active to the two replica instances), I wanted to involve a second additional network. For this I declared a standalone NetworkAttachmentDefinition:
```
apiVersion: "k8s.cni.cncf.io/v1"
kind: NetworkAttachmentDefinition
metadata:
  name: hundredgig
  namespace: default
spec:
  config: '{
            "cniVersion": "0.3.1",
            "name:": "eth2",
            "type": "macvlan",
            "master": "ens2f0",
            "mode": "bridge",
            "ipam": {
                "type": "whereabouts",
                "range":     "172.20.37.0/29"
            }
        }'
```
and Pods can now use annotations to request an IP address on this macvlan bridge network that uses the underlying 100Gb cards (ens2f0) to support a bridge network to connect it to any other Pods in the cluster. In this instance a block of 8 IP addresses has been reserved for use and whose allocation will be tracked by whereabouts. You can specify multiple additional networks by:
```
  annotations:
    k8s.v1.cni.cncf.io/networks: default/tengig,default/hundredgig
```
and when Pods are deployed, the network configuration can be viewed by:
```
oc describe pod/perf0-ibm-mq-1
...
              k8s.v1.cni.cncf.io/networks: default/tengig,default/hundredgig
              k8s.v1.cni.cncf.io/networks-status:
                [{
                    "name": "openshift-sdn",
                    "interface": "eth0",
                    "ips": [
                        "10.130.5.21"
                    ],
                    "default": true,
                    "dns": {}
                },{
                    "name": "default/tengig",
                    "interface": "net1",
                    "ips": [
                        "10.20.37.35"
                    ],
                    "mac": "00:0a:f7:e9:c0:80",
                    "dns": {}
                },{
                    "name": "default/hundredgig",
                    "interface": "net2",
                    "ips": [
                        "172.20.37.5"
                    ],
                    "mac": "4e:0d:ce:54:2c:df",
                    "dns": {}
                }]
```

#### Multus
Once you have created the additional networks, and set the annotations to support IP addresses being assigned to the pods, there is one further problem to resolve. The active and replica QM pods all need to communicate with each other, and to do that without hardwiring addresses, kubernetes services are used. These by default will be on the OpenShift SDN which is our 1Gb network in our setup. We need to use [multus-service](https://cloud.redhat.com/blog/how-to-use-kubernetes-services-on-secondary-networks-with-multus-cni) to redirect the pods to use the service endpoints (endpointslices CRD) on the additional network.

You first need to install the multus-service component. As this is a technology preview, this isnt part of the base OCP project. You also need to be on OCP 4.10+.
```
oc create -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-service/main/deploy-nft.yml
```
Weve already created our definition for the 100GbE in the previous section, so there are only two steps left to do. We need to define the service network as the new `hundredgig` network previously defined. This would usually be set directly on the service, but as the MQ operator creates the service definition for us, we need to alter metadata annotiations in the QueueManager CRD:
```
  annotations:
    k8s.v1.cni.cncf.io/networks: default/tengig,default/hundredgig
    k8s.v1.cni.cncf.io/service-network: default/hundredgig
  labels:
    service.kubernetes.io/service-proxy-name: multus-proxy 
```
We also need to identify that we wish an alternative service proxy implementation is used to provide the endpoints, and the `multus-proxy` implementation is set in the last line above.

When you now deploy your QM (or other pods), additional endpointslices are defined which are utilised in preference to the defaults (which are still defined):
```
oc get endpointslices | grep multus
perf0-ibm-mq-multus-kbpk6             IPv4          1414    172.20.37.1,172.20.37.3,172.20.37.2     14d
perf0-ibm-mq-replica-0-multus-wqvkn   IPv4          9414    172.20.37.2                             14d
perf0-ibm-mq-replica-1-multus-vksfh   IPv4          9414    172.20.37.3                             14d
perf0-ibm-mq-replica-2-multus-p9m9l   IPv4          9414    172.20.37.1                             14d
```
You can check your QM logs to ensure that connectivity exists between the active and replica instances and that they are using the IP addresses on the `hundredgig` additional network:
```
oc logs pod/perf0-ibm-mq-1 | more
...
2023-07-28T18:01:08.150Z AMQ3214I: Native HA inbound secure connection accepted from 'perf0-ibm-mq-0'. [CommentInsert1(perf0-ibm-mq-0), CommentInsert2(172.20.37.2), CommentInsert3(TLS_RSA_WITH_AES_256_GCM_SHA384
)]
2023-07-28T18:01:08.373Z AMQ3214I: Native HA inbound secure connection accepted from 'perf0-ibm-mq-2'. [CommentInsert1(perf0-ibm-mq-2), CommentInsert2(172.20.37.1), CommentInsert3(TLS_RSA_WITH_AES_256_GCM_SHA384
)]
```

### Increasing the pid limit

4.10 UPDATE
At OCP 4.10, the default has yet again changed and after realising their mistake in attempting to force people into restricted PID namespaces, the default PID limit is now back up to 4096.
This (in my testing) should be adequate for 99% of peoples needs, though you can still modify this if required. They are now re-recommending the original workaround of using KubletConfig (which never worked for me) (and not ContainerRuntimeConfig below) if you want to proceed down this path.

OLD (Left for context)
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
Switch to the openshift-machine-config-operator project:
```
oc project openshift-machine-config-operator
oc create -f crio-config.yaml
```
once resource has been created, edit the mcp/worker yaml to apply the configuration, by specifying the matching label to the metadata section:
```
metadata:
  labels:
    config-crio: set-pid
```
This will begin roll out of the updated config across the affected nodes, you can monitor this by:
```
oc get nodes
[mqperf@mqperfx1 openshift]$ oc get nodes
NAME                               STATUS                        ROLES    AGE    VERSION
master1.es02.ocp.hursley.ibm.com   Ready                         master   320d   v1.17.1+1aa1c48
master2.es02.ocp.hursley.ibm.com   Ready                         master   320d   v1.17.1+1aa1c48
master3.es02.ocp.hursley.ibm.com   Ready                         master   320d   v1.17.1+1aa1c48
worker1.es02.ocp.hursley.ibm.com   NotReady,SchedulingDisabled   worker   146d   v1.17.1+1aa1c48
worker2.es02.ocp.hursley.ibm.com   Ready                         worker   149d   v1.17.1+1aa1c48
worker3.es02.ocp.hursley.ibm.com   Ready                         worker   320d   v1.17.1+1aa1c48

oc logs pod/machine-config-controller-85985858cd-x59hm
I1202 15:45:46.366978       1 node_controller.go:758] Setting node worker1.es02.ocp.hursley.ibm.com to desired config rendered-worker-3b625521fd57ee60132b528dd0d2b396
I1202 15:45:46.389985       1 node_controller.go:452] Pool worker: node worker1.es02.ocp.hursley.ibm.com changed machineconfiguration.openshift.io/desiredConfig = rendered-worker-3b625521fd57ee60132b528dd0d2b396
I1202 15:45:47.410225       1 node_controller.go:452] Pool worker: node worker1.es02.ocp.hursley.ibm.com changed machineconfiguration.openshift.io/state = Working
I1202 15:45:47.440930       1 node_controller.go:433] Pool worker: node worker1.es02.ocp.hursley.ibm.com is now reporting unready: node worker1.es02.ocp.hursley.ibm.com is reporting Unschedulable
I1202 15:47:01.278742       1 node_controller.go:433] Pool worker: node worker1.es02.ocp.hursley.ibm.com is now reporting unready: node worker1.es02.ocp.hursley.ibm.com is reporting NotReady=Unknown
```

An update to the OpenShift documentation to communicate this mechanism will made in a future release. There has been a relevant blog discussion on the subject [here](https://www.redhat.com/en/blog/red-hat-openshift-container-platform-4-now-defaults-cri-o-underlying-container-engine)
