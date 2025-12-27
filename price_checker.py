import requests, json, os
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
URL       = os.getenv("HOTEL_URL")

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

html = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

price_tag = soup.select_one('[data-testid="price-and-discounted-price"]')
price = int(price_tag.text.replace("SAR","").replace(",","").strip())

try:
    with open("price.json") as f:
        last = json.load(f)["price"]
except:
    last = 0

if price != last:
    send(f"🔔 Price Changed\nOld: {last} SAR\nNew: {price} SAR\n{URL}")
    with open("price.json","w") as f:
        json.dump({"price":price}, f)
