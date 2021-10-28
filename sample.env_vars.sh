#!/bin/sh
# To deploy notify.py and use it from cron you need to put this in the right place,
# on my system it's ~/.conda/envs/telegram/etc/conda/activate.d/env_vars.sh

export BOT_NAME="your_bots_name"
export BOT_USER="your_bot"
export BOT_TOKEN="THIS PART IS SECRET"

# Account to which messages will be sent.
export CHAT_ID="123412341234"

