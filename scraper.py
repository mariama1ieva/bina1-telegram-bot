import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://textise.net/showtext.aspx?strURL=https://bina.az/items/vipped"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def send(text):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": text
    })


print("Loading bina.az")

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

links = soup.find_all("a")

found = 0

for a in links:

    href = a.get("href")

    if not href:
        continue

    if "/items/" in href and href.split("/")[-1].isdigit():

        link = "https://bina.az" + href

        print("Sending:", link)

        send(link)

        found += 1

        if found == 10:
            break

print("Total:", found)
