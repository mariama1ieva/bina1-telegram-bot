import os
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URLS = [
"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&subwayStation=51&subwayStation=33&subwayStation=54&subwayStation=52&subwayStation=53&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=&groupSimilar=true&search=",

"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&district=74&district=69&district=100&district=91&district=99&district=200&district=75&district=81&district=82&district=85&district=84&district=83&district=92&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=&groupSimilar=true&search=",

"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&orientmark=315&orientmark=385&orientmark=178&orientmark=371&orientmark=179&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=&groupSimilar=true&search=",

"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=Razin&groupSimilar=true&search=",

"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=La%C3%A7%C4%B1n+ticar%C9%99t+m%C9%99rk%C9%99zi&groupSimilar=true&search=",

"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=Ruslan+93&groupSimilar=true&search=",

"https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=Diqlas&groupSimilar=true&search="
]

BLACKLIST = [
"makler",
"vasitəçi",
"vasiteci",
"agent",
"əmlakçı",
"emlakci",
"ofis",
"komissiya",
"xidmət haqqı"
]

KUPCA = [
"kupça",
"kupcali",
"çıxarış",
"cixaris"
]

SEEN_FILE = "seen.json"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


headers = {"User-Agent": "Mozilla/5.0"}

seen = load_seen()

for url in URLS:

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):

        link = a["href"]

        if "/elan/" not in link:
            continue

        full = "https://kub.az" + link

        if full in seen:
            continue

        try:

            ad = requests.get(full, headers=headers)
            text = ad.text.lower()

            if any(w in text for w in BLACKLIST):
                seen.add(full)
                continue

            if not any(w in text for w in KUPCA):
                seen.add(full)
                continue

            send(full)
            seen.add(full)

        except:
            pass

save_seen(seen)
