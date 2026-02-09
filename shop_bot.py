import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

TOKEN = os.getenv("TOKEN")
CHAT_ID = -1003333614856  # твой канал

SHOP_URL = "https://fortnite-api.com/v2/shop/br"

resp = requests.get(SHOP_URL).json()
data = resp["data"]["entries"]

items = []
for entry in data:
    item = entry["items"][0]
    price = entry["finalPrice"]
    rarity = item["rarity"]["displayValue"]
    image = item["images"]["icon"]
    name = item["name"]
    items.append({
        "name": name,
        "price": price,
        "rarity": rarity,
        "image": image
    })

def rarity_color(r):
    return {
        "Common": (180,180,180),
        "Uncommon": (0,255,100),
        "Rare": (80,140,255),
        "Epic": (180,80,255),
        "Legendary": (255,160,60)
    }.get(r, (255,255,255))

def make_collage(chunk, filename):
    cols = 4
    rows = 4
    size = 256
    padding = 20
    title_height = 120

    width = cols*size + (cols+1)*padding
    height = rows*size + (rows+1)*padding + title_height

    bg = Image.new("RGB", (width, height), (30, 60, 120))
    draw = ImageDraw.Draw(bg)

    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
    text = 'Магазин предметов от "Домик Tytyro4ki"'
    draw.text((width//2 - 380, 30), text, fill=(255,220,80), font=title_font)

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

    for i, item in enumerate(chunk):
        row = i // cols
        col = i % cols

        x = padding + col*(size+padding)
        y = title_height + padding + row*(size+padding)

        img = Image.open(BytesIO(requests.get(item["image"]).content)).resize((size, size))
        bg.paste(img, (x,y))

        color = rarity_color(item["rarity"])
        draw.rectangle([x,y,x+size,y+28], fill=color)

        draw.text((x+8, y+4), item["rarity"], fill=(0,0,0), font=font)
        draw.text((x+8, y+size-60), item["name"], fill=(255,255,255), font=font)
        draw.text((x+8, y+size-30), f'{item["price"]} V-Bucks', fill=(255,220,80), font=font)

    bg.save(filename)

half = len(items)//2
make_collage(items[:half], "shop1.png")
make_collage(items[half:], "shop2.png")

def send_photo(path):
    with open(path, "rb") as f:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID},
            files={"photo": f}
        )

send_photo("shop1.png")
send_photo("shop2.png")

print("ГОТОВО. 2 коллажа отправлены.")
