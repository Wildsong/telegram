#!env python
#
import platform
from datetime import datetime
import json
import telegram
from config import Config

hostname = platform.node()
now = datetime.now()
bot = telegram.Bot(token=Config.BOT_TOKEN)

print("send_message")
rval = bot.send_message(chat_id=Config.CHAT_ID, text="Here at %s it's %s." % (hostname, now))
print(rval)

print("send_location")
rval = bot.send_location(chat_id=Config.CHAT_ID, latitude=46.187906, longitude=-123.834518)
print(rval)

print("send_photo")
url="https://piction.clevelandart.org/cma/ump.di?e=1FD7F29C52D63B20747360F6AA0BFC91A8BE622CA9B2DA71B38946D60C50DED9&s=21&se=98193207&v=5&f=2002.89_o2.jpg"
rval = bot.send_photo(chat_id=Config.CHAT_ID, photo=url)
print(rval)




