import os
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import math

TOKEN = os.getenv("TOKEN")
CHAT_ID = -1003333614856  # твой канал

# ===== получаем магазин =====
url = "https://fortnite-api.com/v2/shop/br"
resp = requests.get(url).json()

if not resp.get("data"):
    print("SHOP EMPTY")
    exit()

items = resp["data"]["featured"]["entries"]

# ===== настройки коллажа =====
COLS = 5
CARD_SIZE = 200
PADDING = 20

ROWS = math.ceil(len(items) / COLS)
WIDTH = COLS * CARD_SIZE + PADDING * 2
HEIGHT = ROWS * CARD_SIZE + 140

img = Image.new("RGB", (WIDTH, HEIGHT), "#2b1055")
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 16)
    big = ImageFont.truetype("arial.ttf", 32)
except:
    font = ImageFont.load_default()
    big = font

today = datetime.now().strftime("%d.%m.%Y")
draw.text((20, 20), f"Магазин Fortnite — {today}", fill="white", font=big)

x = PADDING
y = 100

# ===== рисуем карточки =====
for i, entry in enumerate(items):
    item = entry["items"][0]

    name = item["name"]
    price = entry.get("finalPrice", 0)
    icon_url = item["images"]["icon"]

    icon = Image.open(requests.get(icon_url, stream=True).raw)
    icon = icon.resize((CARD_SIZE - 20, CARD_SIZE - 60))

    card = Image.new("RGB", (CARD_SIZE, CARD_SIZE), "#1c1c1c")
    card.paste(icon, (10, 10))

    d = ImageDraw.Draw(card)
    d.text((10, CARD_SIZE - 45), name[:18], fill="white", font=font)
    d.text((10, CARD_SIZE - 25), f"{price} V-Bucks", fill="yellow", font=font)

    img.paste(card, (x, y))

    x += CARD_SIZE
    if (i + 1) % COLS == 0:
        x = PADDING
        y += CARD_SIZE

# ===== сохраняем =====
file = "shop.png"
img.save(file)

# ===== отправляем в Telegram =====
requests.get(
    f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
    params={
        "chat_id": CHAT_ID,
        "photo": "https://raw.githubusercontent.com/"  # заглушка
    },
    files={
        "photo": open(file, "rb")
    }
)

print("COLLAGE SENT")
