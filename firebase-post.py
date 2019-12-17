import requests
import json

from firebase import firebase
firebase = firebase.FirebaseApplication('https://dashboard-cisco.firebaseio.com', None)

result = firebase.get('/dnac', None)
print(result)

data = {'count': 13, 'aps': 9, 'switches': 3, 'routers': 1, 'wlc': 0}
sent = json.dumps(data)
result = firebase.post("/dnac/network-devices/20-12-2019", sent)
print(result)
