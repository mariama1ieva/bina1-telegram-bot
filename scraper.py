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
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


print("Checking bina.az...")

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

ads = soup.find_all("div", class_="items-i")

sent = set()

for ad in ads:

    link_tag = ad.find("a")
    if not link_tag:
        continue

    link = "https://bina.az" + link_tag["href"]

    if link in sent:
        continue

    price = ad.find("div", class_="price-val")
    title = ad.find("div", class_="card-title")

    description = ad.text.lower()

    # Agent filtr
    if "agent" in description or "vasitəçi" in description:
        continue

    price_text = price.text.strip() if price else "No price"
    title_text = title.text.strip() if title else ""

    message = f"{title_text}\n{price_text}\n{link}"

    print("Send:", message)

    send(message)

    sent.add(link)
