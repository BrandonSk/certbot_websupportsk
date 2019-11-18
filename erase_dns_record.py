import hmac
import hashlib
import time
import requests
import base64
import sys
import json
from datetime import datetime

# Script requires positional arguments:
#     1 - apiKey
#     2 - apiSecret
#     3 - domain name
#     4 - record ID

path = "/v1/user/self/zone/" + str(sys.argv[3]) + "/record/" + str(sys.argv[4])

method = "DELETE"
timestamp = int(time.time())
api = "https://rest.websupport.sk"
apiKey = str(sys.argv[1]).encode()
secret = str(sys.argv[2]).encode()

canonicalRequest = "%s %s %s" % (method, path, timestamp)
signature = hmac.new(secret, canonicalRequest.encode('utf-8'), hashlib.sha1).hexdigest()

headers = {
    "Authorization": "Basic %s" % (base64.b64encode( (("%s:%s" % (apiKey.decode('UTF-8'), signature))).encode('UTF-8') ).decode('UTF-8')),
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Date": datetime.fromtimestamp(timestamp).isoformat()
}

url = api + path
response = requests.delete(url, headers=headers).content
print(json.loads(response))
