import os
import re
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/baki/alqi-satqi/menziller?has_bill_of_sale=true&location_ids%5B%5D=51&location_ids%5B%5D=33&location_ids%5B%5D=54&location_ids%5B%5D=52&location_ids%5B%5D=53&location_ids%5B%5D=405&location_ids%5B%5D=378&location_ids%5B%5D=179&location_ids%5B%5D=178&location_ids%5B%5D=100&location_ids%5B%5D=99&location_ids%5B%5D=200&location_ids%5B%5D=74&location_ids%5B%5D=69&location_ids%5B%5D=91&location_ids%5B%5D=81&location_ids%5B%5D=82&location_ids%5B%5D=85&location_ids%5B%5D=84&location_ids%5B%5D=83"

headers = {
    "User-Agent": "Mozilla/5.0"
}

SEEN_FILE = "seen.json"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption,
        "parse_mode": "HTML"
    })


print("Checking bina.az")

seen = load_seen()

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

cards = soup.select(".items-i")

print("Found ads:", len(cards))

for card in cards:

    link_tag = card.select_one("a")
    if not link_tag:
        continue

    href = link_tag.get("href")

    if not re.match(r"^/items/\d+$", href):
        continue

    link = "https://bina.az" + href

    if link in seen:
        continue

    price = card.select_one(".price-val")
    title = card.select_one(".card-title")
    location = card.select_one(".location")
    image = card.select_one("img")

    price_text = price.text.strip() if price else ""
    title_text = title.text.strip() if title else ""
    location_text = location.text.strip() if location else ""

    image_url = image["src"] if image else None

    caption = f"""
🏠 <b>{title_text}</b>

💰 <b>{price_text}</b>

📍 {location_text}

🔗 <a href="{link}">Elanı aç</a>
"""

    print("NEW:", link)

    if image_url:
        send_photo(image_url, caption)

    seen.add(link)

save_seen(seen)
