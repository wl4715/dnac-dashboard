# Dashboard Project
## Aim
Adastral Park is home to British Telecom's (BT) innovation labs and Innovation. BT is looking for a way to showcase the capabilities of Cisco's API when their customers visit these labs. The idea is to display a dashboard in the main reception that shows in real-time the number of users connected to the wifi so that as soon as the customer connects to the network, this number would increase. The customer would be curious on how this technology works and therefore, enable sales. 
## Goal 
We aim to take this idea even further by not only creating a dashboard that showcases the number of users connected in real-time using DNAC but we also, want to expand further into ACI and Meraki. Having a true single plane of glass that allows you to compare the data across these 3 different technologies in regards to devices connected, users connected, etc. In short, creating a realtime network dashboard across all the products that will be displayed, most probably, in a Webex TP. 

## DevNet Github
[DevNet DNAC Github](https://github.com/CiscoDevNet/DNAC-NetworkDevice)

## Adastral Park

url = "dnaccisco-lab.com"

user = "admin"

password = "!!!C1sco123!!!"

## Sandbox environment

url = "https://sandboxdnac2.cisco.com/" (version 1.2.10)
url = "https://sandboxdnac.cisco.com/" (version 1.2.6)

user = "devnetuser"

password = "Cisco123!"

[More sandbox environments version 1.3](https://www.cisco.com/c/dam/en/us/products/se/2019/11/Business_Unit/demo-table.pdf)

## Useful API Endpoints
[DNAC API Documentation](https://developer.cisco.com/docs/dna-center/api/1-3-1-x/)

Get Auth Key = https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token

key = "Authorization"; value = "Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE="

Get Site Health = https://sandboxdnac2.cisco.com/dna/intent/api/v1/site-health

## Firebase
[Firebase Real Time Database](https://dashboard-cisco.firebaseio.com/)
Project name/ Project ID = "dashboard-cisco"

Web API key = "AIzaSyD8szGZGGZsuruITbUe6VWS-vZMq492bKI"

## Pip install
- requests
- python-firebase
