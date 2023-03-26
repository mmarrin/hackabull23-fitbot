import requests
import json
import time
import random

url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/fitbot"
i = 1

while i in range(1, 21):
    ts = str(int(time.time()))
    value = round(random.uniform(51.68, 58.75), 2)
    payload = json.dumps({
        "action": "addreading",
        "name": "Humidity",
        "ownerid": "1",
        "value": str(value),
        "time": ts
    })
    headers = {
        'Content-Type': 'application/json'
    }
    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    time.sleep(5)
    i += 1
