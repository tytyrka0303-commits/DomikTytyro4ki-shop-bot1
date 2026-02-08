import os
import requests
import telebot
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# ===== НАСТРОЙКИ =====
TOKEN = os.getenv("TOKEN")
CHANNEL = "@DomikTytyro4ki"   # свой канал

bot = telebot.TeleBot(TOKEN)

RARITY_COLORS = {
    "common": "#b0b0b0",
    "uncommon": "#1eff00",
    "rare": "#0070dd",
    "epic": "#a335ee",
    "legendary": "#ff8000"
}

# ===== ПОЛУЧЕНИЕ МАГАЗИНА =====
def get_shop():
    url = "https://fortnite-api.com/v2/shop/br"
    try:
        resp = requests.get(url, timeout=10).json()
    except:
        print("API REQUEST FAILED")
        return []

    if "data" not in resp:
        print("API ERROR:", resp)
        return []

    if "featured" not in resp["data"]:
        print("NO FEATURED BLOCK")
        return []

    return resp["data"]["featured"]["entries"]

# ===== ГЕНЕРАЦИЯ КАРТИНКИ =====
def generate_image(items):
    cols = 5
    size = 200
    padding = 20

    rows = (len(items) // cols) + 1
    width = cols * size + padding * 2
    height = rows * size + 150

    img = Image.new("RGB", (width, height), "#2b1055")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
        big = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
        big = font

    today = datetime.now().strftime("%d.%m.%Y")
    draw.text((20, 20), f"Магазин Fortnite - {today}", fill="white", font=big)
    draw.text((20, 70), "DomikTytyro4k1", fill="#ff4dff", font=font)

    x = padding
    y = 120

    for i, entry in enumerate(items):

        if not entry.get("brItems"):
            continue

        item = entry["brItems"][0]
        name = item.get("name", "Unknown")
        price = entry.get("finalPrice", 0)
        rarity = item.get("rarity", {}).get("value", "common")
        color = RARITY_COLORS.get(rarity, "white")
        icon_url = item.get("images", {}).get("icon")

        if not icon_url:
            continue

        try:
            icon = Image.open(
                requests.get(icon_url, stream=True, timeout=10).raw
            )
            icon = icon.resize((size - 20, size - 60))
        except:
            continue

        card = Image.new("RGB", (size, size), color)
        card.paste(icon, (10, 10))

        d = ImageDraw.Draw(card)
        d.text((10, size - 45), name[:16], fill="white", font=font)
        d.text((10, size - 25), f"{price} V-Bucks", fill="yellow", font=font)

        img.paste(card, (x, y))

        x += size
        if (i + 1) % cols == 0:
            x = padding
            y += size

    file = "shop.png"
    img.save(file)
    return file

# ===== ОСНОВНОЙ ЗАПУСК =====
def main():
    print("BOT STARTED")

    if not TOKEN:
        print("TOKEN NOT FOUND")
        return

    items = get_shop()
    if not items:
        print("SHOP EMPTY")
        return

    image = generate_image(items)
    today = datetime.now().strftime("%d.%m.%Y")

    bot.send_photo(
        CHANNEL,
        open(image, "rb"),
        caption=f"🛒 Магазин Fortnite\n📅 {today}\n@DomikTytyro4k1"
    )

    print("SENT SUCCESSFULLY")

main()
