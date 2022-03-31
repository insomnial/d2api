import requests
import os
from dotenv import load_dotenv

load_dotenv()

#dictionary to hold extra headers
HEADERS = {"X-API-Key" : os.getenv('X_API_KEY')}

#make request for Gjallarhorn
r = requests.get("https://www.bungie.net/platform/Destiny/Manifest/InventoryItem/1274330687/", headers=HEADERS);

#convert the json object we received into a Python dictionary object
#and print the name of the item
inventoryItem = r.json()
#print(inventoryItem['Response']['data']['inventoryItem']['itemName'])
print(inventoryItem['Response']['data']['inventoryItem'])

#Gjallarhorn