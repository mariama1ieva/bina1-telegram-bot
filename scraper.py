import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/items/vipped?city_id=1&category_id=1&has_bill_of_sale=true"

ALLOWED_LOCATIONS = [
    "Əhmədli",
    "Həzi Aslanov",
    "Köhnə Günəşli",
    "Yeni Günəşli",
    "Bakıxanov",
    "Qaraçuxur",
    "Günəşli",
    "8-ci kilometr",
    "Massiv A",
    "Massiv B",
    "Massiv D",
    "Massiv G",
    "Massiv V",
    "Qara Qarayev",
    "Neftçilər",
    "Xalqlar Dostluğu",
    "Kristal Abşeron",
    "Laçın ticarət mərkəzi",
    "Neapol dairəsi",
    "Ukrayna dairəsi"
]


def send(msg):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


print("Opening browser")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )

    page = context.new_page()

    page.goto(URL, wait_until="networkidle")

    page.wait_for_timeout(5000)

    cards = page.query_selector_all('[data-cy="item-card"]')

    print("Found ads:", len(cards))

    for card in cards:

        text = card.inner_text().lower()

        allowed = False

        for loc in ALLOWED_LOCATIONS:
            if loc.lower() in text:
                allowed = True
                break

        if not allowed:
            continue

        link = card.query_selector('[data-cy="item-card-link"]')

        if not link:
            continue

        href = link.get_attribute("href")

        full = f"https://bina.az{href}"

        print("Send:", full)

        send(full)

    browser.close()
