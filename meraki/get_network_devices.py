from meraki_sdk.meraki_sdk_client import MerakiSdkClient
from meraki_sdk.exceptions.api_exception import APIException

# Multidomain DevNet sandbox
#x_cisco_meraki_api_key = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

# DevNet Sandbox
x_cisco_meraki_api_key = '15da0c6ffff295f16267f88f98694cf29a86ed87'

meraki = MerakiSdkClient(x_cisco_meraki_api_key)

orgs = meraki.organizations.get_organizations()
#print(orgs)

params = {}
params["organization_id"] = "549236"
nets = meraki.networks.get_organization_networks(params)
#print(nets)

network_id = "L_646829496481104472"
devices = meraki.devices.get_network_devices(network_id)
print(devices)
