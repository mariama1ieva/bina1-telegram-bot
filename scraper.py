import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URLS = [
    "https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=0&ownerType=0&city=1&subwayStation=51&subwayStation=33&subwayStation=54&subwayStation=52&subwayStation=53&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=2&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=&maxPrice=&minArea=&maxArea=&minPricePerSquareMeter=&maxPricePerSquareMeter=&minParcelArea=&maxParcelArea=&words=&groupSimilar=true&search=",
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def parse():
    for url in URLS:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        ads = soup.select(".products-i")[:5]

        for ad in ads:
            title = ad.select_one(".products-name").text.strip()
            link = ad.select_one("a")["href"]

            msg = f"{title}\nhttps://kub.az{link}"
            send_telegram(msg)

if __name__ == "__main__":
    parse()
