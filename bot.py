#
#
#  This is a Telegram bot that listens to messages and responds to them.
#
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import Config
from noaa_sdk import NOAA
import json

print("Here we go!")

def hello(update: telegram.Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

def weather(update: telegram.Update, context: CallbackContext) -> None:
    noaa = NOAA()
    noaa.get_conditions('97103', 'US')
    update.message.reply_text("It's raining")
    res = noaa.get_observations('97103', 'US')
    i = 0
    for item in res:
        print(i, item["presentWeather"])
        i += 1

updater = Updater(Config.BOT_TOKEN)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('weather', weather))

updater.start_polling()
updater.idle()

