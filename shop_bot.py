import requests

TOKEN = "8563120123:AAEhY7ahdvN-_jRYRQZ_fyVbAPzOSRPQLEE"
CHAT_ID = -1003333614856

url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

data = {
    "chat_id": CHAT_ID,
    "photo": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Fortnite_F_letter_logo.png",
    "caption": "Фото пришло — значит всё работает"
}

r = requests.post(url, data=data)
print(r.text)
