import requests, json, os
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
URL       = os.getenv("HOTEL_URL")

def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except Exception as e:
        print("Error sending message:", e)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

html = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

# البحث عن السعر الصحيح للفندق
price_tag = soup.find("div", class_="bui-price-display__value")
if not price_tag:
    print("Error: could not find price on page")
    exit(1)

price_text = price_tag.get_text().strip().replace("EGP","").replace(",","").replace("SAR","")
price = int(''.join(filter(str.isdigit, price_text)))
print("Price found:", price)

try:
    with open("price.json") as f:
        last = json.load(f)["price"]
except:
    last = 0

if price != last:
    send(f"🔔 Price Changed\nOld: {last} SAR\nNew: {price} SAR\n{URL}")
    with open("price.json","w") as f:
        json.dump({"price":price}, f)
