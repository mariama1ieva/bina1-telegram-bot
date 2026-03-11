import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://kub.az/"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def is_agent(item):
    agent = item.find("span", class_="item-owner-type")
    return agent is not None


def has_kupca(item):
    cert = item.find("div", class_="item-certificate")
    return cert is not None


print("Start scraping kub.az")

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

items = soup.find_all("div", class_="item")

for item in items:

    if is_agent(item):
        continue

    if not has_kupca(item):
        continue

    price = item.find("span", class_="price-amount")
    link = item.find("a")

    if price and link:

        price_text = price.text.strip()
        link_text = "https://kub.az" + link["href"]

        message = f"{price_text} AZN\n{link_text}"

        print("Send:", message)

        send(message)
