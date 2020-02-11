import meraki

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

net_id = "L_646829496481104472"

devices = dashboard.devices.getNetworkDevices(net_id)
print(devices)

clients = dashboard.clients.getNetworkClients(net_id)
#print(clients)
