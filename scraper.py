import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/baki/alqi-satqi/menziller?has_bill_of_sale=true&location_ids%5B%5D=51&location_ids%5B%5D=33&location_ids%5B%5D=54&location_ids%5B%5D=52&location_ids%5B%5D=53&location_ids%5B%5D=405&location_ids%5B%5D=378&location_ids%5B%5D=179&location_ids%5B%5D=178&location_ids%5B%5D=100&location_ids%5B%5D=99&location_ids%5B%5D=200&location_ids%5B%5D=74&location_ids%5B%5D=69&location_ids%5B%5D=91&location_ids%5B%5D=81&location_ids%5B%5D=82&location_ids%5B%5D=85&location_ids%5B%5D=84&location_ids%5B%5D=83"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

print("Checking bina.az...")

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

ads = soup.select("a[href*='/items/']")

sent = set()

for ad in ads[:15]:

    link = "https://bina.az" + ad.get("href")

    if link in sent:
        continue

    print("Sending:", link)

    send(link)

    sent.add(link)
