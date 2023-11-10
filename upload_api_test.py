# This python script is run on a local machine 
# and is used to send HTTP requests to the backend to test its performance
# backend can be run locally or on a server e.g. AWS VM


import requests
import json

# List of endpoints: AWS, local
# 13.211.169.215:5000
# 127.0.0.1:5000

# Upload Endpoint
# ------------------------------------------------------------------------
# file for upload test
files = {'file': open('inputs/transcript-retro-B.txt','rb')}
# print(files)


# upload a new file. takes 60-120 seconds to process. Returns ID, name etc.
url = "http://127.0.0.1:5000/uploadtranscript"
r = requests.post(url,data={'name':'test_name_6D','meetingType':'Standup'},files=files)
# ------------------------------------------------------------------------


# Master list of files endpoint
# ------------------------------------------------------------------------
# # Gets the list of all files with ID, name etc.
url = "http://13.211.169.215:5000/masterlist"

r = requests.get(url)
# ------------------------------------------------------------------------



# Get a file specific ID
# ------------------------------------------------------------------------
# request the AI results for a specified file ID e.g. 1
# url = "http://13.211.169.215:5000/files/1"

# r = requests.get(url)
# ------------------------------------------------------------------------


# write output to file if desired
out_file = open("output_test.json", "w")  
    
json.dump(r.json(), out_file, indent = 6)  

out_file.close()

# print statements for easy debugging
# print(r.json())

# print(r.json()['data']["Meta"]['ID'])