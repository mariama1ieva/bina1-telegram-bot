import asyncio
from playwright.async_api import async_playwright
from database import is_new
from notifier import send_message
from config import FILTER_URL

print("STARTED 🚀")


# 🔹 SƏNİN KRİTERİYALAR
ALLOWED_LOCATIONS = [
    "əhmədli", "həzi aslanov", "köhnə günəşli", "yeni günəşli",
    "8-ci kilometr", "bakıxanov", "günəşli", "qaraçuxur",
    "massiv a", "massiv b", "massiv d", "massiv g", "massiv v",
    "qara qarayev", "neftçilər", "xalqlar dostluğu"
]

ALLOWED_LANDMARKS = [
    "kristal abşeron", "laçın ticarət mərkəzi",
    "neapol dairəsi", "ukrayna dairəsi"
]


# 🔹 FILTER FUNCTION
async def is_valid_listing(page):
    text = await page.content()
    text = text.lower()

    # mülkiyyətçi
    if "mülkiyyətçi" not in text:
        return False

    # agent blok
    if "agent" in text or "vasitəçi" in text:
        return False

    # çıxarış
    if "çıxarış" not in text:
        return False

    # location filter
    if not any(loc in text for loc in ALLOWED_LOCATIONS):
        return False

    # landmark (optional)
    if not any(lm in text for lm in ALLOWED_LANDMARKS):
        return False

    return True


# 🔹 DATA PARSE
async def parse_listing(page):
    try:
        # qiymət
        price_el = await page.query_selector(".price-val")
        price = await price_el.inner_text() if price_el else "N/A"

        # otaq
        room_el = await page.query_selector(".product-properties__i-value")
        rooms = await room_el.inner_text() if room_el else "N/A"

        # location
        loc_el = await page.query_selector(".product-map__left__address")
        location = await loc_el.inner_text() if loc_el else "N/A"

        # şəkil
        img_el = await page.query_selector("img[src]")
        image = await img_el.get_attribute("src") if img_el else None

        return price, rooms, location, image

    except:
        return "N/A", "N/A", "N/A", None


async def run():
    print("RUN STARTED 🔥")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
         headless=True,
         args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page = await context.new_page()

        print("Opening page...")
        await page.goto(FILTER_URL, timeout=60000)

        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)

        await page.mouse.wheel(0, 3000)
        await page.wait_for_timeout(3000)

        # 🔥 düzgün linkləri seç
        elements = await page.query_selector_all("a[href^='/items/']")

        ads = []
        for el in elements:
            href = await el.get_attribute("href")

            if href and href.replace("/items/", "").isdigit():
                ads.append(href)

        print("REAL ADS:", len(ads))

        for url in ads[:5]:
            try:
                full_url = "https://bina.az" + url
                print("OPENING:", full_url)

                detail = await context.new_page()
                await detail.goto(full_url, timeout=60000)
                await detail.wait_for_timeout(3000)

                # 🔥 FILTER
                if not await is_valid_listing(detail):
                    print("FILTERED ❌")
                    await detail.close()
                    continue

                print("MATCH FOUND ✅")

                # parse
                price, rooms, location, image = await parse_listing(detail)

                # duplicate check
                if is_new(full_url):
                    message = f"""
🏠 {rooms} otaqlı
💰 {price}
📍 {location}

🔗 {full_url}
"""
                    send_message(message)
                    print("SENT TO TELEGRAM 📩")

                await detail.close()

            except Exception as e:
                print("Error:", e)

        await browser.close()


async def main():
    await run()


asyncio.run(main())