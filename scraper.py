import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API = "https://bina.az/items/vipped"

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


print("Checking bina.az")

r = requests.get(API, headers=headers)

text = r.text

links = []

for part in text.split('"id":'):

    num = ""

    for c in part:

        if c.isdigit():
            num += c
        else:
            break

    if len(num) > 5:

        link = f"https://bina.az/items/{num}"

        if link not in links:
            links.append(link)


print("Found:", len(links))

for link in links[:10]:

    print("Sending:", link)

    send(link)
