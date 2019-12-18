import requests
import json
import datetime

from firebase import firebase
firebase = firebase.FirebaseApplication('https://dashboard-cisco.firebaseio.com', None)

date = datetime.datetime.now().strftime("%x")
date = date.replace("/","-")
print(date)

result = firebase.put('','/dnac/network-devices/{}/routers'.format(date),1)
result = firebase.put('','/dnac/network-devices/{}/switches'.format(date),3)

# post = u-id included

result = firebase.get('/dnac', None)
print(result)
