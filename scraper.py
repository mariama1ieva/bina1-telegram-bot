import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/baki/alqi-satqi/menziller?has_bill_of_sale=true&location_ids%5B%5D=51&location_ids%5B%5D=33&location_ids%5B%5D=54&location_ids%5B%5D=52&location_ids%5B%5D=53&location_ids%5B%5D=405&location_ids%5B%5D=378&location_ids%5B%5D=179&location_ids%5B%5D=178&location_ids%5B%5D=100&location_ids%5B%5D=99&location_ids%5B%5D=200&location_ids%5B%5D=74&location_ids%5B%5D=69&location_ids%5B%5D=91&location_ids%5B%5D=81&location_ids%5B%5D=82&location_ids%5B%5D=85&location_ids%5B%5D=84&location_ids%5B%5D=83"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html",
    "Connection": "keep-alive"
}


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

    print("Telegram:", r.status_code)


print("Checking bina.az")

r = requests.get(URL, headers=headers)

print("Page status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

links = soup.select("a[href*='/items/']")

print("Found ads:", len(links))

for ad in links[:10]:

    link = "https://bina.az" + ad.get("href")

    print("Sending:", link)

    send(link)
