import os
import re
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/baki/alqi-satqi/menziller?has_bill_of_sale=true"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
}

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


print("Loading bina.az")

r = requests.get(URL, headers=headers)

print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

links = soup.select("a")

found = 0

for link in links:

    href = link.get("href")

    if not href:
        continue

    # only real listings
    if not re.match(r"^/items/\d+$", href):
        continue

    full_link = "https://bina.az" + href

    print("Sending:", full_link)

    send(full_link)

    found += 1

    if found >= 10:
        break

print("Total sent:", found)
