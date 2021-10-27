# telegram

Telegram is a messaging system similar to WhatsApp but not owned by Facebook.

I set up this repo to create some tests in Python.
My intention at this time is to use Telegram to send system status information to my phone.

## Set up

Get an account and do the steps to set up a bot.

```bash
cp sample.env .env
emacs .env
conda create -n telegram python python-telegram-bot python-dotenv -c conda-forge
conda activate telegram
python send_message.py
```

If you have set up .env correctly you should see some messages appear on your phone including
one text, one map, and a picture from the Cleveland Art Museum collection.

## Docs

See https://python-telegram-bot.org/

Especially, https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html

