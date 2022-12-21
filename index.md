### MQ Performance documents

This github repository will be used to publish MQ Performance documents from the MQ Performance Team based in Hursley, England.

For many years the traditional place for Performance reports has been the [IBM SupportPac](http://www-01.ibm.com/support/docview.wss?uid=swg27007150) website. 

For new documents and performance articles, we intend to use this repository as the home for MQ Performance collateral.

### MQ Appliance
#### M2002

The M2002 MQ Appliance was released in July 2018, and the accompanying MQ Appliance Performance Report (MPA3) illustrates the increased performance of the new Hardware:
- M2002 Performance Report [MPA3.pdf](./MPA3.pdf)

Whilst MPA3 contrasts the performance of M2002 with the M2001 appliance, the M2002 MQ Appliance Performance Report (MPA4) updates MPA3 with data from MQ 9.2 and also includes data from TLS and AMS scenarios:
- M2002 Performance Report [MPA4.pdf](./MPA4.pdf)

The ability to encrypt the filesystems of an M2002 appliance and thus protecting customer data at rest is supported from MQ 9.2.5. The following report details the performance impact of filesystem encryption for both the M2002A and M2002B models:
- M2002 Filesystem Encryption Report [M2002_9.2.5_Encrypted_Filesystem_Impact.pdf](./M2002_9.2.5_Encrypted_Filesystem_Impact.pdf)

#### M2001

The M2001 MQ Appliance was released in June 2016, and the accompanying MQ Appliance Performance Report (MPA1) and MQ Appliance HA and DR Performance Report (MPA2) have been updated to show the increased performance on the new Hardware:
- M2001 Performance Report [MPA1-2.0.pdf](./MPA1-2.0.pdf)
- ~~M2001 HA and DR Performance Report [MPA2-2.0.pdf](./MPA2-2.0.pdf)~~

The release of MQ 9.1 in July 2018, resulted in performance improvements in many HA and DR related scenarios on the M2001 appliance. The HA and DR Performance report has been updated again to Version 3:
- M2001 HA and DR Performance Report [MPA2-3.0.pdf](./MPA2-3.0.pdf)



#### M2000

The M2000 MQ Appliance was the original version of the MQ Appliance and the performance reports that relate to this model are available here:
- M2000 Performance Report [MPA1.pdf](./MPA1.pdf) 
- M2000 HA and DR Performance Report [MPA2.pdf](./MPA2.pdf) 

#### AMS

MQ V9 delivered a new AMS Quality of Protection called ‘Confidentiality’. A performance whitepaper has been produced that illustrates the performance profile this new mode brings by comparing it to existing AMS, TLS and non AMS scenarios. [AMSMQAppliance.pdf](./AMSMQAppliance.pdf)


### MQ Distributed

#### Best Practises for Performance
This document contains general sections on best practises for performance, formerly included in the performance reports (MQ V8 and earlier). It is now published as a seperate report.[MQ Performance Best Practises V1.0.1](./MQ_Performance_Best_Practices_v1.0.1.pdf)

#### Base MQ (V9.1 onwards)
Performance reports for MQ on distributed platforms from V9.1 onwards are available below.
For reports on versions of distributed MQ prior to V9.1 go to the MQ SupportPac page here [here](http://www-01.ibm.com/support/docview.wss?uid=swg27007150). 

- IBM MQ V9.1 for Linux (x86-64 platform) Performance Report: [MQ_for_xLinux_V9.1_Performance.pdf](./MQ_V9.1_Performance_Report_xLinux.pdf)
- IBM MQ V9.1 for Windows Performance Report: [MQ_for_Windows_V910_Performance.pdf](./MQ_for_Windows_V910_Performance.pdf)
- IBM MQ V9.2 for Linux (x86-64 platform) Performance Report: [MQ_for_xLinux_V9.2_Performance.pdf](./MQ_V9.2_Performance_Report_xLinux.pdf)
- IBM MQ V9.3 for Linux (x86-64 platform) Performance Report: [MQ_for_xLinux_V9.3_Performance.pdf](./MQ_V9.3_Performance_Report_xLinux_v1.pdf)

#### AMS

MQ V9 delivered a new AMS Quality of Protection called ‘Confidentiality’. A performance whitepaper has been produced that illustrates the performance profile this new mode brings by comparing it to existing AMS and non AMS scenarios. [AMS.pdf](./AMS.pdf)

#### Persistent Messaging Performance

A paper describing the best practises for persistent messaging, and illustrating the performance of some different filesytems hosting the MQ transaction log of Linux on x86 has now been released:
[mqio_v1.pdf](./mqio_v1.pdf).

#### RDQM HA Performance

A report illustrating the performance of the high availability (HA) function using RDQM (delivered in the V9.0.4 CD & V9.1 LTs releases of MQ) has been released. The report is based on tests run on Linux for x86, and includes comparisons with the previous software HA offering (MIQM).
[rdqm_performance_1.1.pdf](./rdqm_performance_1.1.pdf).

#### Queue Manager Re-start Times
A paper illustrating some of the important factors that can affect queue manager re-start times after a server failure (for instance). Includes optimisations made in V9.1.1 to improve queue manager recovery. 
[Queue Manager Restart Times.pdf](./Queue%20Manager%20Restart%20Times.pdf).

#### Streaming Queues Performance (Updated on 22nd December 2021 to include sections on using message expiry with streaming queues).
Performance report on streaming queues, introduced in MQ V9.2.3, including a comparison with a Pub/Sub approach to message duplication. [MQ V9.2.3 Streaming Queues Performance Report V1.1.pdf](./MQ%20V9.2.3%20Streaming%20Queues%20Performance%20Report%20V1.1.pdf).


### MQ on OpenShift
MQ is now available as part of the Cloud Pak for Integration (CP4I) available on the OpenShift platform. Whitepapers exploring the performance of MQ in that environment will be published shortly. These will be consumable reports that investigate a particular scenario; choose the most appropriate report to assist you in your sizing process.

Advice on setup and configuration of MQ (CP4I) and running workloads against the deployed QM can be found [here](./openshift/configuration.md)

#### OpenShift 4.2 + CP4I 2019.4.1 (MQ 9.1.4)
The first performance whitepaper on OpenShift looks at the performance of the QM when the client is co-located in the same OpenShift cluster: [MQ on OCP 4.2](./openshift/OCP4.2-InternalMessaging.pdf).


### MQ for z/OS

Performance reports for the latest versions of IBM MQ for z/OS are available here. 
- MQ for z/OS Capacity Planning and Tuning guide [MP16.pdf](./mp16.pdf). This report provides capacity planning and setup/tuning information for IBM MQ for z/OS 9.3 and earlier releases. It describes how to define performance critical queue manager and channel initiator environment parameters. This version includes updates due to DASD upgrades, CFCC level 25, MQ for z/OS 9.3 and some minor tweaks including references to blogs relating to MQ and SMF which is of particular relevance with the ability to increase the frequency of SMF data collection introduced in MQ 9.3.
- MQ for z/OS version 9.0 performance report [MP1K.pdf](./mp1k.pdf). The report discusses the performance of AMS, including the new AMS 'Confidentiality' Quality of Protection, using IBM MQ classes for JMS in both CICS OSGi JVM Server and IMS environments as well as page set statistics. Note MQ for z/OS version 9.0 is now end of support.
- MQ for z/OS version 9.1 performance report [MQ for zOS V910 Performance.pdf](./MQ%20for%20zOS%20V910%20Performance.pdf). The report discusses the performance characteristics of the MQ for z/OS V910 as well the performance improvements to AMS, support for Java clients on z/OS and Db2 Universal Table Space support.
- MQ for z/OS version 9.2 performance report [MQ for zOS V920 Performance.pdf](./MQ_for_zOS_V920_Performance.pdf). This report discusses the performance characteristics of the MQ for z/OS V9.2 release, as well as the performance of the new features including zHyperWrite for active logs, data set encryption support, TLS 1.3 cipher support for MQ channels, and for the Advanced VUE version the support of AMS Interception on server to server channels and the fasp.io gateway running on z/OS Container Extensions.
- MQ for z/OS 9.3 performance report [MQ for zOS 9.3 Performance.pdf](./MQ%20for%20zOS%209.3%20Performance.pdf). This report discusses the performance characteristics of the MQ for z/OS 9.3 release including the performance of new features such as Streaming Queues, Statistics trace class(5) and allowing the data collection interval for accounting trace to be set independently of statistics trace, plus more granular control of the SMF data collection intervals. Updated on 16th December 2022 to include performance data for support of shared queue in Streaming queue feature with APAR PH49686.

#### MQ for z/OS - General white papers

Performance reports for MQ on z/OS documenting our experiences:

- How does MQ for z/OS perform when moving to z16? Paper [MQ for z/OS on z16](./MQ_for_zOS_on_z16.pdf) discusses the performance expectations and what we achieved when moving from IBM z15 to IBM z16. The paper also discusses the changes from CFCC level 25 and the the new Crypto Express 8S feature.
- How does MQ for z/OS perform when moving to z15? Paper [MQ for z/OS on z15](./MQ_for_zOS_on_z15.pdf) discusses the performance expectations and what we achieved when moving from z14 to z15. The paper also discusses some of the new features available on z15 that MQ is able to use, such as the on-chip compression accelerator and the Crypto Express 7S feature.
- How does MQ for z/OS perform when moving to z14? Paper [MQ for z/OS on z14](./MQ_for_zOS_on_z14_v1.2.pdf) discusses the performance expectations and what we achieved when moving from z13 to z14. The paper also discusses some of the new features available on z14 that MQ is able to use such as the Crypto Express 6S feature and the re-location of Storage Class Memory from CF Flash to Virtual Flash Memory. There is also an update to the impact of using zEDC compression with MQ archive logs.
- Performance of streamed persistent workload from z/OS using shared queue to Linux [QREP_Performance_MQ_zOS_to_Linux.pdf](./QREP_Performance_MQ_zOS_to_Linux.pdf). This paper discusses the shared queue configuration options when sending persistent messages to a Linux partner, illustrating differences in performance when the Linux partner uses client or bindings connections. The configuration used simulates a Queue Replication workload.
- With the introduction of z/OS Container Extensions (zCX) which allow clients to deploy Linux on Z applications in Docker containers on z/OS, the [MQ with zCX](./MQ%20with%20zCX.pdf) report discusses the performance of the 3 use cases where zCX can add value to your MQ for z/OS configurations - acting as a client concentrator, a cluster full repository and as a host system for a fasp.io gateway.
- When and why to use channel compression on MQ for z/OS is discussed in paper [MQ for z/OS Channel Compression](./MQforZOS_ChannelCompression.pdf). The paper discusses what compression options are available on IBM z16, including using hardware, why compressing highly compressible messages may actually be more expensive than less compressible messages and when cost savings from compression might be achieved. 


### MFT

IBM MQ Managed file transfer performance report contains the charts showing Performance measurements to present the performance characteristics of MQ V9.0.5 for Linux platform and to assist capacity planning. This report shows the messaging rate that can be achieved on Linux systems when transferring messages using different chunk sizes. Anyone designing, implementing or sizing Managed File Transfer solutions using WebSphere MQ for V9.0.5 and above and needs to understand the performance characteristics on Linux platform should review this report.
- xLinux MFT 9.0.5 Performance Report [Linux-IBM-MQMFT-9.0.5.0-PerformanceReport.pdf](./Linux-IBM-MQMFT-9.0.5.0-PerformanceReport.pdf)
- Windows MFT 9.0.5 Performance Report [Windows-IBM-MQMFT-9.0.5-PerformanceReport.pdf](./Windows-IBM-MQMFT-9.0.5-PerformanceReport.pdf)
- MFT 9.0.5 Performance Report on the number of Standard MFT Agents per Agent Queue Manager [IBM_MQMFT_9.0.5_Performance_Report_MultipleAgentsPerQueueManager_V2.pdf](./IBM_MQMFT_9.0.5_Performance_Report_MultipleAgentsPerQueueManager_V2.pdf)
- MFT 9.1 Performance Report on transfers of Huge file size like 10, 20 or 30 GB [IBM_MQMFT_9.1_Performance_Report_HugeFilesSize_V1.pdf](./IBM_MQMFT_9.1_Performance_Report_HugeFilesSize_V1.pdf)
- MFT 9.0.5 Performance Report of Protocol bridge Agent and Standard Agent when files are transferred across 20+ miles locally and 5000+ miles globally [IBM_MQMFT_9.0.5_Performance%20Report_Protocol_Bridge_Scenario_V3.pdf](./IBM_MQMFT_9.0.5_Performance%20Report_Protocol_Bridge_Scenario_V3.pdf)
- MFT for z/OS version 9.2.0 Performance report [MFT_for_zOS_v920.pdf](./MFT_for_zOS_v920.pdf)

### IBM MQ XMS .NET Client
IBM XMS .NET Client performance report showing Performance measurements of MQ v9.1.x XMS .NET Client's connecting to MQ v9.1 Queue Manager.Performance reports contains .NET Core applications running on Windows and Linux.Where .NET Framework applications are running on Windows machine.
- XMS .NET Core Performance Report [XMS .NET Core Performance Report.pdf](./XMS%20.NET%20Core%20Performance%20Report.pdf)
- XMS .NET Framework Performance Report [XMS .NET Framework Performance Report](./XMS%20.NET%20Framework%20Performance%20Report.pdf)

### FASP
The Fast, Adaptive and Secure Protocol (FASP®) is a high-speed transport that can achieve speeds much higher than TCP, especially across high latency and/or lossy networks. This capability is available through the fasp.io Gateway which MQ V9.1.4 advanced edition customers can download via Passport Advantage. Some initial results measured in the lab for servers channels connecting through a fasp.io Gateway can be seen in [this deck](./MQ914_fasp_gw.pdf). 
**!!18th Feb 2020 - Updated with compression measurements.**

### Test Harnesses and tools
For more information on the test harnesses and tools used to generate the data found in these reports, please take a look at the available [tools](./testharness.md).

### Get in touch
You can contact @stmassey and @pharrishur with questions about the MQ Performance content.

