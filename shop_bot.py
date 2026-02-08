import os
import requests

TOKEN = os.getenv("TOKEN")
CHAT_ID = -1003333614856# твой тгк

url = "https://fortnite-api.com/v2/shop/br"
resp = requests.get(url).json()

if not resp.get("data"):
    print("SHOP EMPTY")
    exit()

items = resp["data"]["featured"]["entries"]

text = "🛒 Магазин Fortnite сегодня:\n\n"

for entry in items[:5]:
    name = entry["items"][0]["name"]
    text += f"• {name}\n"

requests.get(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    params={
        "chat_id": CHAT_ID,
        "text": text
    }
)

print("SENT TO TELEGRAM")
