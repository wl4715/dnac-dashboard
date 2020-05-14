import meraki # Import Meraki SDK
import firebase_admin # Import Firebase Python SDK
from firebase_admin import credentials
from firebase_admin import db
from credentials import home_api_key, home_network_id, mv_serial # Separate file with credentials

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dashboard-cisco.firebaseio.com/'
})
# Authenticate Meraki 
dashboard = meraki.DashboardAPI(
    api_key = home_api_key,
    base_url = 'https://n255.meraki.com/api/v0'
)

# Get the snapshot from a specific timestamp
def get_snapshot_url(time):	
	body = {'timestamp': time, 'fullframe': False}
	snapshot = dashboard.cameras.generateNetworkCameraSnapshot(network_id, serial, **body)
	return snapshot['url']

if __name__ = "__main__":
	photo_url = get_snapshot_url('2020-05-11T06:19:34-07:00')
	# Upload to Firebase
	ref = db.reference('meraki/photoURL/')
	ref.set(photo_url)