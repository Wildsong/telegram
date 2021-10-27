#!env python
#
import platform
from datetime import datetime
import telegram
from config import Config

hostname = platform.node()
bot = telegram.Bot(token=Config.BOT_TOKEN)

print("send_message")
rval = bot.send_message(chat_id=Config.CHAT_ID, text="This is a message from %s." % hostname)
print(rval)

print("send_location")
rval = bot.send_location(chat_id=Config.CHAT_ID, latitude=46.187906, longitude=-123.834518)
print(rval)

print("send_photo")
rval = bot.send_photo(chat_id=Config.CHAT_ID, photo="https://wiki.wildsong.biz/images/2/23/Tenrec.png")
print(rval)




