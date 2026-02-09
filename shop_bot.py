import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import math

TOKEN = os.getenv("TOKEN")
CHAT_ID = -1003333614856

url = "https://fortnite-api.com/v2/shop/br"
resp = requests.get(url).json()

if not resp.get("data"):
    print("API ERROR:", resp)
    exit()

items = resp["data"]["featured"]["entries"]

half = math.ceil(len(items) / 2)
parts = [items[:half], items[half:]]

COLS = 4
SIZE = 300

try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
except:
    font = ImageFont.load_default()

def make_collage(entries, filename):
    rows = math.ceil(len(entries) / COLS)
    canvas = Image.new("RGB", (COLS * SIZE, rows * SIZE), "black")
    draw = ImageDraw.Draw(canvas)

    x = 0
    y = 0

    for entry in entries:
        item = entry["items"][0]
        icon_url = item["images"]["icon"]
        price = entry["finalPrice"]
        rarity = item["rarity"]["displayValue"]

        img_data = requests.get(icon_url).content
        icon = Image.open(BytesIO(img_data)).resize((SIZE, SIZE))
        canvas.paste(icon, (x * SIZE, y * SIZE))

        # редкость сверху
        draw.rectangle(
            (x*SIZE, y*SIZE, x*SIZE+SIZE, y*SIZE+30),
            fill="black"
        )
        draw.text(
            (x*SIZE+10, y*SIZE+5),
            rarity,
            fill="white",
            font=font
        )

        # цена снизу
        draw.rectangle(
            (x*SIZE, y*SIZE+SIZE-35, x*SIZE+SIZE, y*SIZE+SIZE),
            fill="black"
        )
        draw.text(
            (x*SIZE+10, y*SIZE+SIZE-30),
            f"{price} V-Bucks",
            fill="white",
            font=font
        )

        x += 1
        if x >= COLS:
            x = 0
            y += 1

    canvas.save(filename)

make_collage(parts[0], "shop_1.png")
make_collage(parts[1], "shop_2.png")

for file in ["shop_1.png", "shop_2.png"]:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID},
        files={"photo": open(file, "rb")}
    )

print("SHOP SENT WITH PRICES & RARITY")
