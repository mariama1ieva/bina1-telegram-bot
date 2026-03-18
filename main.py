import asyncio
from playwright.async_api import async_playwright
from scraper import get_random_proxy
from parser import is_owner
from database import is_new
from notifier import send_message
from config import FILTER_URL, CHECK_INTERVAL

async def run():
    async with async_playwright() as p:

        proxy_url = get_random_proxy()

        browser = await p.chromium.launch(
            headless=True,
            proxy={"server": proxy_url}
        )

        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(FILTER_URL)

        ads = await page.query_selector_all(".items-i")

        for ad in ads:
            try:
                link_el = await ad.query_selector("a.items-i__link")
                url = await link_el.get_attribute("href")
                full_url = "https://bina.az" + url

                detail = await context.new_page()
                await detail.goto(full_url)

                if not await is_owner(detail):
                    await detail.close()
                    continue

                if is_new(full_url):
                    send_message(f"🏠 Yeni mülkiyyətçi elanı:\n{full_url}")

                await detail.close()

            except Exception as e:
                print("Error:", e)

        await browser.close()


async def main():
    while True:
        await run()
        await asyncio.sleep(CHECK_INTERVAL)


asyncio.run(main())
