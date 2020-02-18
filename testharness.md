# Test Harnesses

We use a number of different test harnesses and tools in our testing of MQ. Many of which have been made publicly available via open-source.

There are two different messaging test applications
1.  [CPH](https://github.com/ibm-messaging/mq-cph)            C Based Test Harness utilising the MQI API
2.  [JMSTestHarness](https://github.com/ot4i/perf-harness)    JMS Based Test Harness

These have been containerized into simple to run tools:
1.  [cphtestp](https://github.com/ibm-messaging/cphtestp)     Containerized version of CPH
2.  [jmstestp](https://github.com/ibm-messaging/jmstestp)     Containerized version of JMSTestHarness

There is also a tool for testing your IO performance (in the manner in which MQ writes) called MQLDT (MQ Log Disk Tester).

This also now has a containerized version available here [mqldt-c](https://github.com/ibm-messaging/mqldt-c) and the automatically built
image is available from docker hub [https://hub.docker.com/repository/docker/stmassey/mqldt]. This image can be easily obtained by:
```
docker pull stmassey/mqldt
```
