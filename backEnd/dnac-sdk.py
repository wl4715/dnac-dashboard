from dnacentersdk import api
from credentials import dnac_url, username, password
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dashboard-cisco.firebaseio.com/'
})

dnac = api.DNACenterAPI(base_url = dnac_url, username = username, password = password)

# Function to get devices in the network
def get_devices_family():
	devices = dnac.devices.get_device_list()
	device_family = []
	for device in devices.response:
	    device_family.append(device['family'])
	return device_family

# Define new function to get the client health
def setup_custom():
    dnac.custom_caller.add_api('get_client_health',
                            lambda:
                                dnac.custom_caller.call_api(
                                    'GET',
                                    '/dna/intent/api/v1/client-health',

                                    ).response
                            )

# Function that takes the path and the value and pushes it to Firebase    
def push_to_firebase(path, value):
	# True: Retrieve current time in year/month/day/hour/minute
	# if True:
	# 	date = str(datetime.now().strftime("%Y%m%d%H%M"))
	# # False: Retrieve current time in year/month/day
	# else:
	date = str(datetime.now().strftime("%Y%m%d"))

	# Define the Path
	ref = db.reference(path+date)
	# Set the value
	ref.set(value)


if __name__ == "__main__":

	device_family = get_devices_family()
	print(device_family)
	
	# Get number of devices per model 
	routers = device_family.count('Routers')
	switches = device_family.count('Switches and Hubs')
	wireless_controller = device_family.count('Wireless Controller')
	access_point = device_family.count('Unified AP')

	# Add the custom API calls to the connection object under the custom_caller wrapper
	setup_custom()

	# Call the newly added function to get the client health
	client_health = dnac.custom_caller.get_client_health()[0]['scoreDetail']

	# Print Total Client Count
	print('total client count', client_health[0]['clientCount'])

	# Wired Clients
	wired_clients = client_health[1]['clientCount']

	# Wireless Clients
	wireless_clients = client_health[2]['clientCount']

	# Wireless Clients Status Score
	wireless_clients_poor = client_health[2]['scoreList'][0]['clientCount']
	wireless_clients_fair = client_health[2]['scoreList'][1]['clientCount']
	wireless_clients_good = client_health[2]['scoreList'][2]['clientCount']

	# Push to Firebase
	push_to_firebase('dnac/networkDevices/aps/', access_point)
	push_to_firebase('dnac/networkDevices/wlc/', wireless_controller)
	push_to_firebase('dnac/networkDevices/sw/', switches)
	push_to_firebase('dnac/networkDevices/routers/', routers)
	push_to_firebase('dnac/networkClients/wired/', wired_clients)
	push_to_firebase('dnac/networkClients/wireless/', wireless_clients)
	push_to_firebase('dnac/networkClients/wireless_score/poor', wireless_clients_poor)
	push_to_firebase('dnac/networkClients/wireless_score/fair', wireless_clients_fair)
	push_to_firebase('dnac/networkClients/wireless_score/good', wireless_clients_good)