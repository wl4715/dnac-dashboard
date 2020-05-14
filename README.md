# Dashboard Project
## Aim
Adastral Park is home to British Telecom's (BT) innovation labs and Innovation. BT is looking for a way to showcase the capabilities of Cisco's API when their customers visit these labs. The idea is to display a dashboard in the main reception that shows in real-time the number of users connected to the wifi so that as soon as the customer connects to the network, this number would increase. The customer would be curious on how this technology works and therefore, enable sales.
## Goal
We aim to take this idea even further by not only creating a dashboard that showcases the number of users connected in real-time using DNAC but we also, want to expand further into ACI and Meraki. Having a true single plane of glass that allows you to compare the data across these 3 different technologies in regards to devices connected, users connected, etc. In short, creating a realtime network dashboard across all the products that will be displayed, most probably, in a Webex TP.

## Overview of the solution
![Overview of the solution](/Game_Plan.jpeg)

## Backend
### DevNet Github
[DevNet DNAC Github](https://github.com/CiscoDevNet/DNAC-NetworkDevice)

[New Meraki SDK](https://github.com/meraki/dashboard-api-python)

[DNA Center SDK](https://github.com/cisco-en-programmability/dnacentersdk)

[Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)

### Pip install
- requests
- python-firebase ** deprecated
- firebase-admin
- meraki-sdk ** deprecated
- meraki
- dnacentersdk

## Firebase 
https://dashboard-cisco.firebaseio.com/
