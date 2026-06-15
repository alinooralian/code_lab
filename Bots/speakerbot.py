import telebot
from gtts import gTTS
import os
import uuid

API_TOKEN = ""

def text_to_sound(text, output_file):
    myobj = gTTS(text, lang = "en", slow = False)
    myobj.save(output_file)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! یه جمله بفرست تا برات ویس بسازم...")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "در حال ساخت ویس... ⏳")
    file_name = str(uuid.uuid4()) + ".mp3"
    text_to_sound(message.text, file_name)
    with open(file_name, 'rb') as voice_file:
        bot.send_audio(
            message.chat.id,
            voice_file
        )
    
    bot.reply_to(message, "ویس آماده شد ✅")
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
        except:
            pass

bot.infinity_polling()