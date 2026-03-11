import os
import json
import requests
from urllib.parse import urlparse, parse_qs

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SEARCH_URLS = [
"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&subwayStation=51&subwayStation=33&subwayStation=54&subwayStation=52&subwayStation=53&documentType=-1&loanType=-1&minFloor=2&maxFloor=31",
"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&district=74&district=69&district=100&district=91&district=99&district=200&district=75&district=81&district=82&district=85&district=84&district=83&district=92",
"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&words=Razin",
"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&words=Diqlas"
]

BLACKLIST = [
"makler",
"vasitəçi",
"vasiteci",
"agent",
"əmlakçı",
"emlakci",
"komissiya",
"xidmət haqqı"
]

KUPCA_WORDS = [
"kupça",
"kupcali",
"çıxarış",
"cixaris"
]

SEEN_FILE = "seen_ads.json"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def parse_query(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    params = {}

    for k, v in qs.items():
        params[k] = v[0]

    return params


def get_ads(params):

    API = "https://kub.az/api/ads/search"

    r = requests.get(API, params=params, timeout=30)

    if r.status_code != 200:
        return []

    data = r.json()

    if "ads" not in data:
        return []

    return data["ads"]


def is_agent(text):
    t = text.lower()
    return any(w in t for w in BLACKLIST)


def has_kupca(text):
    t = text.lower()
    return any(w in t for w in KUPCA_WORDS)


def main():

    seen = load_seen()

    for search_url in SEARCH_URLS:

        params = parse_query(search_url)

        ads = get_ads(params)

        for ad in ads[:20]:

            ad_id = str(ad.get("id"))

            if ad_id in seen:
                continue

            title = ad.get("title", "")
            description = ad.get("description", "")
            price = ad.get("price", "")
            url = f"https://kub.az/elan/{ad_id}"

            text = (title + " " + description).lower()

            if is_agent(text):
                seen.add(ad_id)
                continue

            if not has_kupca(text):
                seen.add(ad_id)
                continue

            message = f"{title}\nQiymət: {price}\n{url}"

            send_telegram(message)

            seen.add(ad_id)

    save_seen(seen)


if __name__ == "__main__":
    main()
