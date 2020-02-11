import meraki
import pandas as pd
import datetime
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dashboard-cisco.firebaseio.com', None)

api_key = '15da0c6ffff295f16267f88f98694cf29a86ed87'

dashboard = meraki.DashboardAPI(
    api_key = api_key,
    base_url = 'https://api-mp.meraki.com/api/v0'
)

def get_network_devices(network_id):

    devices = dashboard.devices.getNetworkDevices(network_id)

    device_model = []
    for dev in devices:
        device_model.append(dev['model'])

    print(device_model)

    count = len(device_model)

    device_family = ['MR']
    mr = sum(any(m in L for m in device_family) for L in device_model)

    device_family = ['MS']
    ms = sum(any(m in L for m in device_family) for L in device_model)

    device_family = ['MX']
    mx = sum(any(m in L for m in device_family) for L in device_model)

    return count, mr, ms, mx

##---------------------------------------------------------------

if __name__ == "__main__":
    net_id = "L_646829496481104472"
    total, aps, sw, rout = get_network_devices(net_id)
    print(total, aps, sw, rout)

    date = datetime.datetime.now().strftime("%x")
    date = date.replace("/","-")

    result = firebase.put('','/meraki/devices/count/{}'.format(date),total)
    result = firebase.put('','/meraki/devices/mx/{}'.format(date),rout)
    result = firebase.put('','/meraki/devices/ms/{}'.format(date),sw)
    result = firebase.put('','/meraki/devices/mr/{}'.format(date),aps)
