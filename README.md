# OpenDXL-ATD-NSM

This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and McAfee NSM. McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will subscribe and parse IP indicators ATD produced and will quarantine suspicious IP's on McAfee IPS Sensors via the McAfee NSM.
