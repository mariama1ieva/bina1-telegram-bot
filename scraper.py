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

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })


print("Checking bina.az...")

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

ads = soup.find_all("div", class_="items-i")

for ad in ads[:10]:

    link_tag = ad.find("a")
    img_tag = ad.find("img")
    price_tag = ad.find("div", class_="price-val")
    title_tag = ad.find("div", class_="card-title")

    if not link_tag:
        continue

    link = "https://bina.az" + link_tag["href"]

    image = img_tag["src"] if img_tag else None
    price = price_tag.text.strip() if price_tag else ""
    title = title_tag.text.strip() if title_tag else ""

    caption = f"{title}\n{price}\n{link}"

    print("Send:", caption)

    if image:
        send_photo(image, caption)
