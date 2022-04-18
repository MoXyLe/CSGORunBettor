import requests
import json
import time

f = open("data.txt", "a+")

for i in range(2051791, 2053001):
    try:
        response = requests.get("https://api.csgorun.pro/games/" + str(i), timeout = 25)

        data = json.loads(response.text)

        f.write(str(i) + " " + str(data["data"]["crash"]) + "\n")

        time.sleep(0.2)

        print(i)
    except Exception as e:
        time.sleep(60)

        response = requests.get("https://api.csgorun.pro/games/" + str(i), timeout = 25)

        data = json.loads(response.text)

        f.write(str(i) + " " + str(data["data"]["crash"]) + "\n")

        time.sleep(0.2)

        print(e)

f.close()
