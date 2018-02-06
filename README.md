### MQ Performance documents

This github repository will be used to publish MQ Performance documents from the MQ Performance Team based in Hursley, England.

For many years the traditional place for distributed Performance reports has been the [IBM SupportPac](http://www-01.ibm.com/support/docview.wss?uid=swg27007150) website. 

For new documents and performance articles, we intend to use this repository as the home for MQ Performance collateral.

### MQ Appliance
#### M2001

The M2001 MQ Appliance was released in June 2016, and the accompanying MQ Appliance Performance Report (MPA1) MQ Appliance HA and DR Performance Report (MPA2) have been updated to show the increased performance on the new Hardware:
- M2001 Performance Report [MPA1-2.0.pdf](./MPA1-2.0.pdf)
- M2001 HA and DR Performance Report [MPA2-2.0.pdf](./MPA2-2.0.pdf)

#### M2000

The M2000 MQ Appliance was the original version of the MQ Appliance and the performance reports that relate to this model are available here:
- M2000 Performance Report [MPA1.pdf](./MPA1.pdf) 
- M2000 HA and DR Performance Report [MPA2.pdf](./MPA2.pdf) 

#### AMS

MQ V9 delivered a new AMS Quality of Protection called ‘Confidentiality’. A performance whitepaper has been produced that illustrates the performance profile this new mode brings by comparing it to existing AMS, TLS and non AMS scenarios. [AMSMQAppliance.pdf](./AMSMQAppliance.pdf)


### MQ Distributed

We intend to publish future versions of the MQ base performance documents.

#### AMS

MQ V9 delivered a new AMS Quality of Protection called ‘Confidentiality’. A performance whitepaper has been produced that illustrates the performance profile this new mode brings by comparing it to existing AMS and non AMS scenarios. [AMS.pdf](./AMS.pdf)

#### Persistent Messaging Performance

A paper describing the best practises for persistent messaging, and illustrating the performance of some different filesytems hosting the MQ transaction log of Linux on x86 has now been released:
[mqio_v1.pdf](./mqio_v1.pdf).

### MQ for z/OS

Performance reports for the latest version of IBM MQ for z/OS will initially be published both here and on the [IBM SupportPac](http://www-01.ibm.com/support/docview.wss?uid=swg27007150) website. 
- MQ for z/OS Capacity Planning and Tuning guide [MP16.pdf](./mp16.pdf). This report provides capacity planning and setup/tuning information for IBM MQ for z/OS version 9.0 and earlier releases. It describes how to define performance critical queue manager and channel initiator environment parameters. This version of the report includes LOGLOAD considerations, queue manager restart, CFCC level 21 and the updated IMS Preload module list.
- MQ for z/OS version 9.0 performance report [MP1K.pdf](./mp1k.pdf). The report discusses the performance of AMS, including the new AMS 'Confidentiality' Quality of Protection, using IBM MQ classes for JMS in both CICS OSGi JVM Server and IMS environments as well as page set statistics.
- MQ for z/OS version 9.0.1 performance report [V901.pdf](./V901.pdf). The report discusses the performance improvements to AMS as part of the first Continuous Delivery release.
- Performance of streamed persistent workload from z/OS using shared queue to Linux [QREP_Performance_MQ_zOS_to_Linux.pdf](./QREP_Performance_MQ_zOS_to_Linux.pdf). This paper discusses the shared queue configuration options when sending persistent messages to a Linux partner, illustrating differences in performance when the Linux partner uses client or bindings connections. The configuration used simulates a Queue Replication workload.


### Get in touch
You can contact @stmassey and @pharrishur with questions about the MQ Performance content.

