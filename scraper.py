import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/items/vipped?city_id=1&category_id=1&has_bill_of_sale=true"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def send_photo(photo, caption):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })

print("Loading page...")

r = requests.get(URL, headers=headers)
print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

cards = soup.select('[data-cy="item-card"]')
print("Found:", len(cards))

for card in cards[:10]:
    link_tag = card.select_one('[data-cy="item-card-link"]')
    price_tag = card.select_one('[data-cy="item-card-price-full"]')
    img_tag = card.select_one("img")

    if not link_tag:
        continue

    link = "https://bina.az" + link_tag["href"]
    price = price_tag.text.strip() if price_tag else ""
    image = img_tag["src"] if img_tag else ""

    text = f"{price}\n{link}"

    print("Sending:", link)

    if image:
        send_photo(image, text)
