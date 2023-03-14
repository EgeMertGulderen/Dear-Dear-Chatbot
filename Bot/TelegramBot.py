import telebot
from Training import chat
bot = telebot.TeleBot("5928664554:AAEdE6aqRnoxYvG-YyPSwsbMNcEpAlWqPpA")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba ben Dear Deer, size nasıl yardımcı olabilirim?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    den = chat(message.text)
    bot.reply_to(message, den)

bot.infinity_polling()
