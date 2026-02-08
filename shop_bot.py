import telebot
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# временно твой личный id
CHAT_ID = 123456789  # <-- сюда свой id от @userinfobot

bot.send_message(CHAT_ID, "ТЕСТ: если видишь это сообщение — бот работает")
print("SENT")
