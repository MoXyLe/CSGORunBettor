import json
import requests
import telegram_send
import time

lastNumber = 0

for i in range(1, 1000000):
    print(i)

    response = requests.get("https://api.csgorun.pro/current-state", timeout = 15)

    data = json.loads(response.text)

    if data["data"]["game"]["history"][0]["crash"] < 1.2 and data["data"]["game"]["history"][0]["id"] != lastNumber:
        lastNumber = data["data"]["game"]["history"][0]["id"]
        telegram_send.send(messages=["Go!"])

    time.sleep(5)
