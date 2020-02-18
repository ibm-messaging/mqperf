# Test Harnesses

We use a number of different test harnesses and tools in our testing of MQ. Many of which have been made publicly available via open-source.

There are two different messaging test applications
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

There is also a tool for testing your IO performance (in the manner in which MQ writes) called [MQLDT](https://github.com/ibm-messaging/mqldt) (MQ Log Disk Tester).

This also now has a containerized version available here [mqldt-c](https://github.com/ibm-messaging/mqldt-c) and the automatically built
image is available from docker hub https://hub.docker.com/repository/docker/stmassey/mqldt. This image can be easily obtained by:
```
docker pull stmassey/mqldt
```
