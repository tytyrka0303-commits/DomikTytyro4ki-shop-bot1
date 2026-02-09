import os
import requests

TOKEN = os.getenv("TOKEN")
CHAT_ID = -1003333614856

if not TOKEN:
    print("❌ TOKEN не найден")
    exit()

url = "https://api.telegram.org/bot" + TOKEN + "/sendPhoto"

data = {
    "chat_id": CHAT_ID,
    "photo": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Fortnite_F_letter_logo.png",
    "caption": "✅ Бот работает, фото отправлено"
}

r = requests.post(url, data=data)

print(r.text)
