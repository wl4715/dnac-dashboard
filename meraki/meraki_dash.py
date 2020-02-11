import meraki
import pandas as pd

api_key = '15da0c6ffff295f16267f88f98694cf29a86ed87'

dashboard = meraki.DashboardAPI(
    api_key = api_key,
    base_url = 'https://api-mp.meraki.com/api/v0'
)

orgs = dashboard.organizations.getOrganizations()
#print(orgs)

org_id = "549236"
nets = dashboard.networks.getOrganizationNetworks(org_id)
#print(nets)

net_id = "L_646829496481104495"

clients = dashboard.clients.getNetworkClients(net_id)
print(clients)

devices = dashboard.devices.getNetworkDevices(net_id)
#print(devices)

device_model = []
for dev in devices:
    device_model.append(dev['model'])

print(device_model)

device_list = pd.Series(device_model)
device_family = ['MR', 'MS', 'MX', 'MV']

count = device_list.str.contains('|'.join(device_family)).sum()

print(count)
