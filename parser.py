async def is_owner(page):
    el = await page.query_selector(".product-owner__info-region")
    if not el:
        return False

    text = (await el.inner_text()).lower()

    if "mülkiyyətçi" in text:
        return True

    return False
