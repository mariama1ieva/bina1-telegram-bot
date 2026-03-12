import os
import json
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bina.az/baki/alqi-satqi/menziller?has_bill_of_sale=true"

SEEN_FILE = "seen_ads.json"

ALLOWED_LOCATIONS = [
    "əhmədli","həzi aslanov","köhnə günəşli","yeni günəşli","bakıxanov",
    "qaraçuxur","günəşli","8-ci kilometr","massiv a","massiv b","massiv d",
    "massiv g","massiv v","qara qarayev","neftçilər","xalqlar dostluğu",
    "kristal abşeron","laçın ticarət mərkəzi","neapol dairəsi","ukrayna dairəsi"
]


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(data):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(data), f)


def send_photo(photo, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption,
        "parse_mode": "HTML"
    })


seen = load_seen()

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

    page.goto(URL, wait_until="domcontentloaded", timeout=60000)

    page.wait_for_timeout(4000)

    # daha çox elan yüklə
    page.mouse.wheel(0, 15000)
    page.wait_for_timeout(4000)

    cards = page.query_selector_all('[data-cy="item-card"]')

    print("Found ads:", len(cards))

    for card in cards[:25]:

        text = card.inner_text().lower()

        # agent filter
        if "vasitəçi" in text or "agent" in text or "agentlik" in text:
            print("Skip agent")
            continue

        location_found = None

        for loc in ALLOWED_LOCATIONS:
            if loc in text:
                location_found = loc
                break

        if not location_found:
            print("Skip location")
            continue

        link = card.query_selector('[data-cy="item-card-link"]')

        if not link:
            continue

        href = link.get_attribute("href")

        if not href:
            continue

        full = f"https://bina.az{href}"

        if full in seen:
            print("Skip duplicate")
            continue

        price = card.query_selector('[data-cy="item-card-price-full"]')
        price_text = price.inner_text() if price else ""

        img = card.query_selector("img")
        img_url = img.get_attribute("src") if img else ""

        caption = f"""
🏠 <b>Mənzil tapıldı</b>

📍 <b>{location_found.title()}</b>
💰 <b>{price_text}</b>

🔗 <a href="{full}">Elana bax</a>
"""

        print("Send:", full)

        if img_url:
            send_photo(img_url, caption)

        seen.add(full)

save_seen(seen)
