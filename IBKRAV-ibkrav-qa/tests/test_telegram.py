from telegram import Bot
import os

bot = Bot(token=os.getenv("BOT_TOKEN"))
print("Bot inicializado correctamente.")
