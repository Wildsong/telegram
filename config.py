import os

class Config(object):
#    import dotenv
#    load_dotenv()

    BOT_NAME = os.environ.get("BOT_NAME")
    BOT_USER = os.environ.get("BOT_USER")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")

if __name__ == '__main__':
    
    assert(len(Config.BOT_NAME))
    assert(len(Config.BOT_USER))
    assert(len(Config.BOT_TOKEN))
    assert(len(Config.CHAT_ID))


    
