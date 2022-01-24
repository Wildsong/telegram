# telegram

Telegram is a messaging system similar to WhatsApp but not owned by Facebook.

I set up this repo to create some tests in Python.
My intention at this time is to use Telegram to send system status information to my phone.

## Set up

Get an account and do the steps to set up a bot.

FIXME, config.py should be able to handle either test or deploy modes.

In testing I did something like this,

```bash
cp sample.env .env
emacs .env
```

In deployment I do something like this

```bash
mkdir -p ~/.conda/envs/telegram/etc/conda/activate.d
cp sample.env_vars.sh ~/.conda/envs/telegram/etc/conda/activate.d/env_vars.sh
emacs ~/.conda/envs/telegram/etc/conda/activate.d/env_vars.sh
chmod +x ~/.conda/envs/telegram/etc/conda/activate.d/env_vars.sh
```

```bash
conda create -n telegram python python-telegram-bot python-dotenv -c conda-forge
conda activate telegram
python send_message.py
```

If you have set up .env correctly you should see some messages appear on your phone including
one text, one map, and a picture from the Cleveland Art Museum collection.

## Healthcheck

The scripts healthcheck.py is currently tuned for my servers, 
it checks file mount points and urls from lists that are embedded in it.

If run with "-v" it generates a report on everything it's checked.
It will always generate an error report if anything fails.
It sends the report via Telegram and "print", the intention
is to run it regularly from crontab and it will generate both
messages and emails.

FIXME -- I might make it more general purpose someday. A YAML file, those are popular. Or JSON.

### Deploy healthceck.py

Set up the conda environment as for "notify.py" and put the script on your path. Call it from crontab.

```bash
cp healthcheck.py config.py ~/bin
```

## bot

Accepts commands and responds to them. The commands are

```bash
/hello
/weather
```

Install the noaa-sdk package to read weather conditions.

```bash
pip install noaa-sdk
```

## Docs

See https://python-telegram-bot.org/

Especially, https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html

