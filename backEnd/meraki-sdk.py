import meraki # Import Meraki SDK
from datetime import datetime # Import Date & Time Library
import firebase_admin # Import Firebase Python SDK
from firebase_admin import credentials
from firebase_admin import db
from credentials import meraki_api_key, network_id # Separate file with credentials

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dashboard-cisco.firebaseio.com/'
})

# Initialize Meraki Dashboard with api_key authentication
dashboard = meraki.DashboardAPI(
    api_key = meraki_api_key,
    base_url = 'https://api-mp.meraki.com/api/v0'
)

# Get Network Devices Models
def get_devices_model():
	devices = dashboard.devices.getNetworkDevices(network_id)
	device_model = []
	for device in devices:
		device_model.append(device['model'][:2])
	return device_model

# Function that takes the path, the value, the data and the time format 
# and pushes to Firebase  
def push_to_firebase(path, value, time_format):
	# Get the current time
	date = str(datetime.now().strftime(time_format))
	# Define the Path
	ref = db.reference(path+date)
	# Set the value
	ref.set(value)

if __name__ == '__main__':

	device_model = get_devices_model()
	print(device_model)

	# Get number of devices per model 
	mr = device_model.count('mr')
	ms = device_model.count('ms')
	mx = device_model.count('mx')
	mv = device_model.count('mv')
	mg = device_model.count('mg')


	Ymd = "%Y%m%d" # Year/Month/Date
	YmdHM = "%Y%m%d%H%M" # Year/Month/Date/hour/minute

	# Push to Firebase
	push_to_firebase('dnac/networkDevices/mr/', mr, Ymd)
	push_to_firebase('dnac/networkDevices/ms/', ms, Ymd)
	push_to_firebase('dnac/networkDevices/mx/', mx, Ymd)
	push_to_firebase('dnac/networkDevices/mv/', mv, Ymd)
	push_to_firebase('dnac/networkDevices/mg/', mg, Ymd)

	# push_to_firebase('meraki/networkClients/online/', online_clients, YmdHM)
	# push_to_firebase('meraki/networkClients/offline/', offline_clients, YmdHM)
	# push_to_firebase('meraki/networkClients/online/', wireless_clients, YmdHM)
	# push_to_firebase('meraki/networkClients/OS/Mac/', mac_users, YmdHM)
	# push_to_firebase('meraki/networkClients/OS/Windows/', windows_users, YmdHM)
	# push_to_firebase('meraki/networkClients/OS/Linux/', linux_users, YmdHM)