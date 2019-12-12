import requests
import json

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
    print("total number of devices: ", count)

    access_point = device_family.count('Unified AP')
    switches = device_family.count('Switches and Hubs')
    wireless_controller = device_family.count('Wireless Controller')
    routers = device_family.count('Routers')

    print("access points: ", access_point)
    print("switches and hubs: ", switches)
    print("wireless controllers: ", wireless_controller)
    print("routers: ", routers)

##---------------------------------------------------------------

if __name__ == "__main__":
    token = get_auth_token()
    get_network_device(token)
