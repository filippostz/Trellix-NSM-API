#!/usr/bin/env python

import requests
import sys
import base64
import json
import os
import ipaddress

nsm = ''  # Enter the NSM IP address
duration = 15  # Enter the duration time to quarantine a system
user = ''  # Enter the username
pw = ''  # Enter the password

requests.packages.urllib3.disable_warnings()

def readFile(sourceFilePath):
    if os.path.isfile(sourceFilePath) and os.access(sourceFilePath, os.R_OK):
        with open(sourceFilePath) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
            return lines
    else:
        return False

def b64(user, password):
    authstring = user + ':' + password
    authstring = authstring.encode('utf-8')
    return base64.b64encode(authstring)

def ip_address_check(ip):
   try:
       ipaddress.ip_address(ip)
       return True
   except:
       return False

def session(nsm, user, password):
    authheader = {
        'Accept': 'application/vnd.nsm.v1.0+json',
        'Content-Type': 'application/json',
        'NSM-SDK-API': b64(user, password)
    }
    try:
        r = requests.get('https://%s/sdkapi/session' % nsm, headers=authheader, timeout=10, verify=False)
    except:
        print("NSM not reachable!")
        sys.exit(1)
    if r.status_code == 200:
        print('Successfully authenticated')
    else:
        print('Something went wrong during the authentication')
        sys.exit(1)

    res = r.json()
    sessionheader = {
        'Accept': 'application/vnd.nsm.v1.0+json',
        'Content-Type': 'application/json',
        'NSM-SDK-API': b64(res['session'], res['userId'])
    }
    return sessionheader


def get_sensors(nsm, sessionheader):
    r = requests.get('https://%s/sdkapi/sensors' % nsm, headers=sessionheader, verify=False)
    res = r.json()
    return res


def is_sensorup(sensor_id, sessionheader):
    r = requests.get('https://%s/sdkapi/sensor/%s/status' % (nsm, sensor_id), headers=sessionheader, verify=False)
    res = r.json()

    try:
        if res['status'] == 'ACTIVE':
            return True
    except:
        return False

    return False


def get_qhosts(nsm, sensor_id, sessionheader):
    r = requests.get('https://%s/sdkapi/sensor/%s/action/quarantinehost' % (nsm, sensor_id), \
                     headers=sessionheader, verify=False)
    res = r.json()
    return res


def post_qhost(ip_address, sensor_id, duration, sessionheader):
    time = {15: 'FIFTEEN_MINUTES', 30: 'THIRTY_MINUTES', 45: 'FORTYFIVE_MINUTES', 60: 'SIXTY_MINUTES',
            240: 'FOUR_HOURS', 480: 'EIGHT_HOURS', 720: 'TWELVE_HOURS', 960: 'SIXTEEN_HOURS',
            999: 'UNTIL_EXPLICITLY_RELEASED'}

    if duration not in time: duration = 15

    payload = {
        'IPAddress': '%s' % ip_address,
        'Duration': '%s' % time[duration]
    }

    qhosts = get_qhosts(nsm, sensor_id, sessionheader)

    try:
        for ip in qhosts['QuarantineHostDescriptor']:
            ip = ip['IPAddress']
            if ip_address == ip:
                print('Host is already quarantined')
                return
    except:
        pass

    if sensor_id and is_sensorup(sensor_id, sessionheader):
        r = requests.post('https://%s/sdkapi/sensor/%s/action/quarantinehost' % (nsm, sensor_id), headers=sessionheader,
                          data=json.dumps(payload), verify=False)
        res = r.json()
        if r.status_code == 200:
            print('Added the IP %s to the quarantine successfully' % ip_address)
        else:
            print('Something went wrong during the quarantine update')
    elif is_sensorup(sensor_id, sessionheader) == False:
        print('Sensor %s down, does not exit or model not supported' % sensor_id)
        res=0
    return res


def disconnect(nsm, sessionheader):
    r = requests.delete('https://%s/sdkapi/session' % nsm, headers=sessionheader, verify=False)
    if r.status_code == 200:
        print('Successfully logged out')
    else:
        print('Something went wrong during logout.')
    return r


if __name__ == "__main__":

    if len(sys.argv) > 1:
        ip_list = readFile(sys.argv[1])
        if ip_list:
            connect = session(nsm, user, pw)
            sensors = get_sensors(nsm, connect)
            print('Available Sensors with ID are posted below')
            print('-------------------')
            for i in sensors['SensorDescriptor']:
                model = i['model']
                ip = i['sensorIPAddress']
                sensorid = i['sensorId']
                print("    Model: %s   |   Sensor IP Address: %s  |   SensorID: %s " % (
                    i['model'], i['sensorIPAddress'], str(i['sensorId'])))
                print('-------------------')
                for ip in ip_list:
                    ip=ip.rstrip()
                    if ip_address_check(ip):
                        post_qhost(ip, sensorid, duration, connect)
                    else:
                        print("Invalid IP")
            disconnect = disconnect(nsm, connect)
        else:
            print("File containing a list of IPs missing")

    else:
        print("File containing a list of IPs missing")

