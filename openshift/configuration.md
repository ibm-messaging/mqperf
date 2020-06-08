## OpenShift Configuration
This document contains guidance on setting up an MQ QM (as part of CP4I) and running an MQ workload against the QM. 
The relevant yaml that was used in the configuration will be provided and any limitations (and workarounds) will be documented to define
the environment used for the openshift performance whitepapers.

### CP4I Deployment


### Additional network configuration
The default SDN (Software Defined Network) for our OCP 4.2 cluster uses 1Gb networking for all its communication between master->workers as well as workers->workers and external clients->workers. This obviously creates a network bottleneck when testing. We have a 10GbE network  available across our cluster and clients, so we need to take advantage of this. This should be possible using the Multus CNI plugin.  

### Increasing the pid limit
The default value for pids_limit in the CRI-O environment which OpenShift 4 now supports is 1024 user processes. 
This has been reduced from the default 4096 found in docker runtime environments. It seems there isnt a straightforward approach to reconfiguring this value to support more threads. I initially tried to configure podPidsLimit in the same way as configuring maxPods, by the application of a KubletConfiguration:
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
 
The way to increase the pid limit is via the /etc/crio/crio.conf file deployed on each worker node. There is a mechanism where you can base64 encode the entire crio.conf file and overwrite the existing file as part of a MachineConfig, but this appears clumsy and isnt future proof as will override any subsequent changes to crio.conf. Ive raised the following [bugzilla](https://bugzilla.redhat.com/show_bug.cgi?id=1844447) on this issue. In the meantime, Ive adopted the following to enable large numbers of threads to be used by both my client application and the QM.

Select a worker node to deploy your client onto, ssh onto the worker node(you will need access to the bastion node) and manually change the crio.conf to a larger value. Whilst you are logged onto the worker node, restart the crio service 'sudo systemctl restart crio'. You will then need to modify your job/pod yaml to ensure that node is chosen.

```
      nodeSelector: 
        kubernetes.io/hostname : <worker1.hostname.com>
```

A similar approach can be taken for editing the crio.conf on the Node the QM is running on. After restarting the crio service, delete the pod. In my testing, the same node was invariably used to recreate the QM pod.
