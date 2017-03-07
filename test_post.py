from urllib.request import Request, urlopen
import base64
import json
from pprint import pprint

# url = 'http://localhost:5000/image'
url = 'https://mu.yrck.nl/image'

username = 'yorick'
password = ''
merged_auth = base64.b64encode((username + ':' + password).encode())

with open('grumpy.jpg', 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode()

json_data = {'image': encoded_image}

request = Request(url)
request.add_header('Content-Type', 'application/json')
request.add_header('Authorization', b'Basic ' + merged_auth)

with urlopen(request, data=json.dumps(json_data).encode()) as response:
    pprint(json.loads(response.read().decode()))
