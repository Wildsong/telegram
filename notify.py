#!/usr/bin/env -S conda run -n telegram --no-capture-output python
#
#  Send a message received on STDIN via Telegram.
#  Put the ID of the recipient in the .env file.
#  The message can be up to 4096 bytes.
#
#  For example, cat notify.py | python notify.py
#
import sys
import telegram
from config import Config

bot = telegram.Bot(token=Config.BOT_TOKEN)

fp = sys.stdin
message = ''.join(fp.readlines(4096))
if len(message):
    bot.send_message(chat_id=Config.CHAT_ID, text=message)
#else:
#    print("nothing to send")
    
