## Test Harnesses

We use a number of different test harnesses and tools in our testing of MQ. Many of which have been made publicly available via open-source.

There are two different messaging test applications:
*  [CPH](https://github.com/ibm-messaging/mq-cph)            
C Based Test Harness utilising the MQI API
*  [JMSTestHarness](https://github.com/ot4i/perf-harness)    
JMS Based Test Harness

These have been containerized into simple to run tools:
*  [cphtestp](https://github.com/ibm-messaging/cphtestp)     
Containerized version of CPH
*  [jmstestp](https://github.com/ibm-messaging/jmstestp)     
Containerized version of JMSTestHarness

These repositories contain Dockerfiles and instructions to help you create the required Docker images, you need to provide MQ (the freely available Developer Edition is fine) and accept the license conditions. Its because of these restrictions that we cannot make the built images publicly available.

### JMeter
JMeter can also be used with MQ (though we recommend CPH or JMSTestHarness above). If you intend to use JMeter, it's important to configure it correctly as some existing guidance on use with MQ is not optimal. Each thread connecting to MQ should have it's own session, for instance. We have provided a sample JMeter script with instructions [here](./jmeter), to get you started developing your own. 

## IO Testing

There is also a tool for testing your IO performance (in the manner in which MQ writes) called [MQLDT](https://github.com/ibm-messaging/mqldt) (MQ Log Disk Tester).

This also now has a containerized version available here [mqldt-c](https://github.com/ibm-messaging/mqldt-c) and the automatically built
image is available from docker hub at [https://hub.docker.com/repository/docker/stmassey/mqldt](https://hub.docker.com/repository/docker/stmassey/mqldt). This image can be easily obtained by:
```
docker pull stmassey/mqldt
```


## Network testing

iperf3 is the latest incarnation of the popular network testing tool and we use it frequently to check network performance between servers. A containerized version has been made available which can be used in both local docker/podman runtimes and also in Kubernetes/OpenShift environments: 
* [iperf3-server](https://github.com/ibm-messaging/iperf3-server)
* [iperf3-client](https://github.com/ibm-messaging/iperf3-client)
