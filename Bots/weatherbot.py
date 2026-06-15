import telebot
import requests

API_TOKEN = ""

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! please send a location...")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    location = [message.location.latitude, message.location.longitude]
    respone = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location[0]}&longitude={location[1]}&current=temperature_2m,relative_humidity_2m")
    bot.reply_to(message, f"Temp: {respone.json()["current"]["temperature_2m"]}\nHumidity: {respone.json()["current"]["relative_humidity_2m"]}")



bot.infinity_polling()