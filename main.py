import asyncio
from playwright.async_api import async_playwright
from database import is_new
from notifier import send_message
from config import FILTER_URL

print("STARTED 🚀")


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


async def is_valid_listing(page):
    try:
        text = await page.content()
        text = text.lower()

        # ❌ agent blok
        if "agent" in text or "vasitəçi" in text:
            return False

        # ✅ mülkiyyətçi
        if "mülkiyyətçi" not in text:
            return False

        # ✅ çıxarış
        if "çıxarış" not in text:
            return False

        # ✅ rayon / metro (mütləq)
        if not any(loc in text for loc in ALLOWED_LOCATIONS):
            return False

        # ⚠️ nişangah (yumşaq filter)
        if not any(lm in text for lm in ALLOWED_LANDMARKS):
            print("No landmark ⚠️ (keçiririk)")

        return True

    except:
        return False


async def parse_listing(page):
    try:
        price_el = await page.query_selector(".price-val")
        price = await price_el.inner_text() if price_el else "N/A"

        room_el = await page.query_selector(".product-properties__i-value")
        rooms = await room_el.inner_text() if room_el else "N/A"

        loc_el = await page.query_selector(".product-map__left__address")
        location = await loc_el.inner_text() if loc_el else "N/A"

        return price, rooms, location

    except:
        return "N/A", "N/A", "N/A"


async def run():
    print("RUN STARTED 🔥")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        context = await browser.new_context()
        page = await context.new_page()

        print("Opening page...")

        try:
            await page.goto(FILTER_URL, timeout=60000)
        except:
            print("Page load failed ❌")
            await browser.close()
            return

        # 🔥 crash etməyən wait
        try:
            await page.wait_for_selector("a[href^='/items/']", timeout=15000)
        except:
            print("Fallback wait...")
            await page.wait_for_timeout(5000)

        elements = await page.query_selector_all("a[href^='/items/']")

        ads = []
        for el in elements:
            href = await el.get_attribute("href")

            if href and href.replace("/items/", "").isdigit():
                ads.append(href)

        ads = list(set(ads))

        print("ADS FOUND:", len(ads))

        for url in ads[:15]:  # daha çox yoxlayırıq
            try:
                full_url = "https://bina.az" + url
                print("OPENING:", full_url)

                detail = await context.new_page()
                await detail.goto(full_url, timeout=60000)
                await detail.wait_for_timeout(2000)

                if not await is_valid_listing(detail):
                    print("FILTERED ❌")
                    await detail.close()
                    continue

                print("MATCH FOUND ✅")

                price, rooms, location = await parse_listing(detail)

                if is_new(full_url):
                    message = f"""
🏠 {rooms} otaqlı mənzil
💰 {price}
📍 {location}

🔗 {full_url}
"""
                    send_message(message)
                    print("SENT TO TELEGRAM 📩")

                await detail.close()

            except Exception as e:
                print("DETAIL ERROR:", e)

        await browser.close()


async def main():
    print("MAIN STARTED ⚡")

    while True:
        try:
            await run()
        except Exception as e:
            print("MAIN ERROR:", e)

        await asyncio.sleep(600)


asyncio.run(main())