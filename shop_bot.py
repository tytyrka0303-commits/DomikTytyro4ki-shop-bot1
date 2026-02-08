import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

CHAT_ID = -1003333614856# твой реальный id

try:
    bot.send_message(CHAT_ID, "ПРОВЕРКА: бот жив")
    print("OK: message sent")
except Exception as e:
    print("SEND ERROR:", e)
