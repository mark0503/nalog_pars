import telebot as telebot

from config import TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)


bot.polling()
