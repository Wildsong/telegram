#telegram

Telegram is a messaging system similar to WhatsApp but not owned by Facebook.

## Set up

Get an account and do the steps to set up a bot.

```bash
cp sample.env .env
emacs .env
conda create -n telegram python python-telegram-bot python-dotenv -c conda-forge
conda activate telegram
python send_message.py
```

## Docs

See https://python-telegram-bot.org/

Especially, https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html

