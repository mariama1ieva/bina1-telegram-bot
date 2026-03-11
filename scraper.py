import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URLS = [
    "https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&subwayStation=51&subwayStation=33&subwayStation=54&subwayStation=52&subwayStation=53&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=&groupSimilar=true&search=",
]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

print("Script started")

headers = {
    "User-Agent": "Mozilla/5.0"
}

for url in URLS:
    print("Checking:", url)

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a", href=True)

    found = 0

    for a in links:
        link = a["href"]

        if "/elan/" in link:
            full_link = "https://kub.az" + link
            print("Found:", full_link)

            send(full_link)

            found += 1

        if found >= 5:
            break
