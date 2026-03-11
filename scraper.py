import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/baki/alqi-satqi/menziller?has_bill_of_sale=true&location_ids%5B%5D=51&location_ids%5B%5D=33&location_ids%5B%5D=54&location_ids%5B%5D=52&location_ids%5B%5D=53&location_ids%5B%5D=405&location_ids%5B%5D=378&location_ids%5B%5D=179&location_ids%5B%5D=178&location_ids%5B%5D=100&location_ids%5B%5D=99&location_ids%5B%5D=200&location_ids%5B%5D=74&location_ids%5B%5D=69&location_ids%5B%5D=91&location_ids%5B%5D=81&location_ids%5B%5D=82&location_ids%5B%5D=85&location_ids%5B%5D=84&location_ids%5B%5D=83"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def send_photo(photo, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })

    print("Telegram:", r.status_code)


print("Loading bina.az")

r = requests.get(URL, headers=headers)

print("Page status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

cards = soup.select(".items-i")

print("Found ads:", len(cards))

for card in cards[:10]:

    link_tag = card.select_one("a")
    img_tag = card.select_one("img")
    price_tag = card.select_one(".price-val")

    if not link_tag:
        continue

    link = "https://bina.az" + link_tag["href"]

    price = price_tag.text.strip() if price_tag else ""

    image = img_tag["src"] if img_tag else None

    caption = f"{price}\n{link}"

    print("Sending:", link)

    if image:
        send_photo(image, caption)
