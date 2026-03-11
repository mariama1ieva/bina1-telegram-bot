import os
import requests
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://bina.az/items/all"

params = {
    "city_id": 1,
    "category_id": 1,
    "has_bill_of_sale": "true"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


print("Checking bina.az API")

r = requests.get(API_URL, headers=headers, params=params)

data = r.text

print("Response length:", len(data))

items = []

try:
    items = json.loads(data)["items"]
except:
    print("JSON parse failed")

print("Found items:", len(items))

for item in items[:10]:

    item_id = item["id"]

    link = f"https://bina.az/items/{item_id}"

    price = item["price"]

    text = f"{price} AZN\n{link}"

    print("Sending:", link)

    send(text)
