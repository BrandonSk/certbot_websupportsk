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
#     4 - record name      ($ACMC)
#     5 - record content   ($CERTBOT_VALIDATION)

path = "/v1/user/self/zone/" + str(sys.argv[3]) + "/record"

method = "POST"
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

my_data = {"type":"TXT", "name":str(sys.argv[4]), "content":str(sys.argv[5]), "ttl":"600"}

url = api + path
response = requests.post(url, headers=headers, json=my_data).content
r = json.loads(response)
print(r["item"]["id"])
