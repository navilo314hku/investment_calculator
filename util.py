import os 
import json
import requests

def CreateFolderIfNotExist(directory):
    if not os.path.exists(directory):
        # Create the directory
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        print(f"Directory already exists: {directory}")
def GetJsonDictFromUrl(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Access the JSON data from the response
        json_data = response.json()
        print(f"sucessfully get json from {url}")
        return json_data
    else: 
        print('Error:', response.status_code)
        return -1


