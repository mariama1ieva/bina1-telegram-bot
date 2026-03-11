import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/items/vipped?city_id=1&category_id=1&has_bill_of_sale=true"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption,
        "parse_mode": "HTML"
    })


print("Checking bina.az")

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

ads = soup.select('[data-cy="item-card"]')

print("Found:", len(ads))

for ad in ads[:10]:

    link_tag = ad.select_one('[data-cy="item-card-link"]')
    price_tag = ad.select_one('[data-cy="item-card-price-full"]')
    location_tag = ad.select_one('.sc-8bfc75d7-15')
    info_tag = ad.select_one('.sc-8bfc75d7-16')
    img_tag = ad.select_one("img")

    if not link_tag:
        continue

    link = "https://bina.az" + link_tag["href"]

    price = price_tag.text.strip() if price_tag else ""
    location = location_tag.text.strip() if location_tag else ""
    info = info_tag.text.strip() if info_tag else ""

    img = img_tag["src"] if img_tag else ""

    caption = f"""
🏠 <b>{price} AZN</b>

📍 {location}
📊 {info}

🔗 {link}
"""

    print("Sending:", link)

    send_photo(img, caption)
