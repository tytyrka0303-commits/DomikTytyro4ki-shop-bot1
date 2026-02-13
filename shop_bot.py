import requests

TOKEN = "8563120123:AAEhY7ahdvN-_jRYRQZ_fyVbAPzOSRPQLEE"
CHAT_ID = -1003333614856

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "✅ Бот живой и работает!"
}

r = requests.post(url, data=data)
print(r.text)
