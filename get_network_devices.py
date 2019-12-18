import requests
import json
import datetime
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dashboard-cisco.firebaseio.com', None)

host = "https://sandboxdnac2.cisco.com"
## change to any host/sandbox environment
### authorization may be different

def get_auth_token():

    url = host+"/dna/system/api/v1/auth/token%20"

    querystring = {"Authorization":"Basic%20ZGV2bmV0dXNlcjpDaXNjbzEyMyE=%20"}

    headers = {
        'Authorization': "Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE=",
        'cache-control': "no-cache",
        'Postman-Token': "39a9f684-1091-4ba8-a930-8530457edee5"
        }

    response = requests.request("POST", url, headers=headers, params=querystring)

    token = response.json()['Token']

    return token


def get_network_device(token):

    url = host+"/api/v1/network-device"

    headers = {
        'x-auth-token': token,
        'cache-control': "no-cache",
        'Postman-Token': "473c4a26-9270-41ad-be37-954f2d82e4fa"
        }

    response = requests.request("GET", url, headers=headers)

    device_json = response.json()

    device_family = []

    for device in device_json['response']:
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

    result = firebase.get('/dnac', None)
    print(result)
