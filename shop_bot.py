import os
import requests
from PIL import Image
from io import BytesIO
import math

TOKEN = os.getenv("TOKEN")
CHAT_ID = -1003333614856

url = "https://fortnite-api.com/v2/shop/br"
data = requests.get(url).json()["data"]["featured"]["entries"]

# делим магазин на 2 части
half = math.ceil(len(data) / 2)
parts = [data[:half], data[half:]]

COLS = 4
SIZE = 256

def make_collage(items, filename):
    rows = math.ceil(len(items) / COLS)
    canvas = Image.new("RGB", (COLS * SIZE, rows * SIZE), "black")

    x = 0
    y = 0

    for entry in items:
        icon_url = entry["items"][0]["images"]["icon"]
        img_data = requests.get(icon_url).content
        icon = Image.open(BytesIO(img_data)).resize((SIZE, SIZE))

        canvas.paste(icon, (x * SIZE, y * SIZE))

        x += 1
        if x >= COLS:
            x = 0
            y += 1

    canvas.save(filename)

# создаём 2 картинки
make_collage(parts[0], "shop_1.png")
make_collage(parts[1], "shop_2.png")

# отправляем в Telegram
for file in ["shop_1.png", "shop_2.png"]:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID},
        files={"photo": open(file, "rb")}
    )

print("BOTH COLLAGES SENT")
