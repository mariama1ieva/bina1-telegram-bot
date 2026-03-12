import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/items/vipped?city_id=1&category_id=1&has_bill_of_sale=true"

def send(msg):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

print("Opening browser...")

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL)

    page.wait_for_selector('[data-cy="item-card"]')

    cards = page.query_selector_all('[data-cy="item-card"]')

    print("Found:", len(cards))

    for card in cards[:10]:

        link = card.query_selector('[data-cy="item-card-link"]')

        if not link:
            continue

        href = link.get_attribute("href")

        full_link = f"https://bina.az{href}"

        print("Sending:", full_link)

        send(full_link)

    browser.close()
