import requests
import json
import datetime
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dashboard-cisco.firebaseio.com', None)

host = "https://sandboxdnac.cisco.com"
## change to any host/sandbox environment
### authorization may be different

def get_auth_token():

    url = host+"/dna/system/api/v1/auth/token%20"

    headers = {
        'Authorization': "Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE=",
    }

    response = requests.request("put", url, headers=headers).json()

    token = response['Token']

    return token


def get_network_device(token):

    url = host+"/api/v1/network-device"

    headers = {
        'x-auth-token': token,
    }

    response = requests.request("GET", url, headers=headers).json()

    device_family = []

    for device in response['response']:
        device_family.append(device['family'])

    count = len(device_family)
    routers = device_family.count('Routers')
    switches = device_family.count('Switches and Hubs')
    wireless_controller = device_family.count('Wireless Controller')
    access_point = device_family.count('Unified AP')

    return count, routers, switches, wireless_controller, access_point



##---------------------------------------------------------------

if __name__ == "__main__":
    token = get_auth_token()
    device_count, routers, switches, wlc, aps  = get_network_device(token)

    print("total number of devices: ", device_count)
    print("routers: ", routers)
    print("switches and hubs: ", switches)
    print("wireless controllers: ", wlc)
    print("access points: ", aps)

    date = datetime.datetime.now().strftime("%x")
    date = date.replace("/","-")
    print(date)

    result = firebase.put('','/dnac/network-devices/{}/count'.format(date),device_count)
    result = firebase.put('','/dnac/network-devices/{}/routers'.format(date),routers)
    result = firebase.put('','/dnac/network-devices/{}/switches'.format(date),switches)
    result = firebase.put('','/dnac/network-devices/{}/wlc'.format(date),wlc)
    result = firebase.put('','/dnac/network-devices/{}/aps'.format(date),aps)

    #result = firebase.put('','/dnac/devices/date/{}'.format(date),date)
    result = firebase.put('','/dnac/devices/count/{}/'.format(date),device_count)
    result = firebase.put('','/dnac/devices/routers/{}/'.format(date),routers)
    result = firebase.put('','/dnac/devices/switches/{}/'.format(date),switches)
    result = firebase.put('','/dnac/devices/wlc/{}/'.format(date),wlc)
    result = firebase.put('','/dnac/devices/aps/{}/'.format(date),aps)

    result = firebase.get('/dnac', None)
    print(result)
