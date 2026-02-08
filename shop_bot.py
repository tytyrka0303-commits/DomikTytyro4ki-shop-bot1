import os
import telebot
import requests
import os
import telebot
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@DomikTytyro4ki"

bot = telebot.TeleBot(TOKEN)

RARITY_COLORS = {
    "common": "#b0b0b0",
    "uncommon": "#1eff00",
    "rare": "#0070dd",
    "epic": "#a335ee",
    "legendary": "#ff8000"
}

def get_shop():
    url = "https://fortnite-api.com/v2/shop/br"
    return requests.get(url).json()["data"]["featured"]["entries"]

def generate_image(items):
    cols = 5
    size = 200
    padding = 20

    rows = (len(items) // cols) + 1
    width = cols * size + padding * 2
    height = rows * size + 140

    img = Image.new("RGB", (width, height), "#2b1055")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
        big = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
        big = font

    today = datetime.now().strftime("%d.%m.%Y")

    draw.text((20, 20), f"Магазин Fortnite — {today}", fill="white", font=big)
    draw.text((20, 70), "Домик Tytyro4ki", fill="#ff4dff", font=font)

    x = padding
    y = 100

    for i, entry in enumerate(items):
        item = entry["items"][0]
        name = item["name"]
        price = entry["finalPrice"]
        rarity = item["rarity"]["value"]
        color = RARITY_COLORS.get(rarity, "white")

        icon_url = item["images"]["icon"]
        icon = Image.open(requests.get(icon_url, stream=True).raw)
        icon = icon.resize((size-20, size-60))

        card = Image.new("RGB", (size, size), color)
        card.paste(icon, (10, 10))

        d = ImageDraw.Draw(card)
        d.text((10, size-45), name[:16], fill="white", font=font)
        d.text((10, size-25), f"{price} V-Bucks", fill="yellow", font=font)

        img.paste(card, (x, y))

        x += size
        if (i + 1) % cols == 0:
            x = padding
            y += size

    file = "shop.png"
    img.save(file)
    return file

def main():
    items = get_shop()
    image = generate_image(items)
    today = datetime.now().strftime("%d.%m.%Y")
    bot.send_photo(
        CHANNEL,
        open(image, "rb"),
        caption=f"🛒 Магазин Fortnite\n📅 {today}\nДомик Tytyro4ki"
    )

main()
