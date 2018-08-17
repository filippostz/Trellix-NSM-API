# OpenDXL-ATD-NSM
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and McAfee NSM. McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will subscribe and parse IP indicators ATD produced and will quarantine suspicious IP's on McAfee IPS Sensors via the McAfee NSM.

## Component Description

**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly 
identify malicious content and provides local threat intelligence. ATD exports IOC data in STIX format in several ways including the DXL.
https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**McAfee NSM** gives visibility and control over all McAfee IPS sensors deployed across the enterprise network. https://www.mcafee.com/us/products/network-security-platform.aspx

## Prerequisites
McAfee ATD solution (tested with ATD 4.4.2)

Requests ([Link](http://docs.python-requests.org/en/master/user/install/#install))

OpenDXL SDK ([Link](https://github.com/opendxl/opendxl-client-python))
```sh
git clone https://github.com/opendxl/opendxl-client-python.git
cd opendxl-client-python/
python setup.py install
```

McAfee ePolicy Orchestrator, DXL Broker

McAfee NSM 9.1.x (will also work with older NSM versions)

## Configuration
McAfee ATD receives files from multiple sensors like Endpoints, Web Gateways, Network IPS or via Rest API. 
ATD will perform malware analytics and produce local threat intelligence. After an analysis every indicator of comprise will be published via the Data Exchange Layer (topic: /mcafee/event/atd/file/report). 

### atd_subscriber.py
The atd_subscriber.py receives DXL messages from ATD, filters out discovered IP's and loads nsm.py.

Change the CONFIG_FILE path in the atd_subscriber.py file.

`CONFIG_FILE = "/path/to/config/file"`

### nsm.py
The nsm.py script will be executed to push the suspicious IP to the McAfee NSM.

Change the line 8 to 12 in the nsm.py script.
<img width="612" alt="screen shot 2018-08-17 at 14 21 44" src="https://user-images.githubusercontent.com/25227268/44265938-ed64d500-a228-11e8-84d3-05dda608984f.png">

If you don't know the sensor id of your IPS. Uncomment line 115 to 123 and execute the script.
The print out provides you with an overview of all available sensors including their IDs.
Update the ID in line 9 accordingly.

## Run the OpenDXL wrapper
> python atd_nsm_sub.py

or

> nohup python atd_nsm_sub.py &

## Summary
With this use case, ATD produces local intelligence that is immediatly updating policy enforcement points like the 
Network IPS Systems with malicious IP's.
