import sys
import os
import platform
from glob import glob
import requests
from requests.sessions import merge_setting
import telegram
from config import Config
from datetime import datetime

msg = ""
errors = ""
now = datetime.now()

def check_folders(mountpoint):
    """
    Check this volume mounted by looking for files in it.
    """
    global msg, errors

    # These are mount points for folders on cc-files server,
    # the mount points always exist but have files in them if they are
    # working correctly.
    files = glob(mountpoint + "/*")
    if len(files)==0:
        errors += "Mount point problem \"%s\"\n" % mountpoint
        return 1

    count = len(files)
    msg += "Mount point \"%s\" " % mountpoint
    if count: 
        msg += "%d files; GOOD\!" % count
    msg += "\n"

def check_url(url,name):
    """
    Make sure there is a web server running.
    """
    global msg, errors

    # Note, you can set timeout to .001 to test timeouts.
    # Normally it should be high enough to accomodate slow services
    # such as the map proxy.
    t = 20 
    try:
        r = requests.get(url, timeout=t, verify=False)
        if r.status_code == 200: 
            msg += "%s [%s](%s)\n" % (str(r.elapsed), name, url)
            return 0
        errors += "Status code %s on [%s](%s)\n" % (r.status_code, name, url)

    except requests.exceptions.Timeout:
        errors += "Timeout on [%s](%s)\n" % (name, url)
        
    except requests.exceptions.ConnectionError:
        errors += "Connection failed [%s](%s)\n" % (name, url)

    except Exception as e:
        errors += "999999 Unkempt error\n" + e

def telegram_escape(t):
    """ Telegram objects to some characters and wants them escaped. """
    t = t.replace(')', '\)')
    t = t.replace('(', '\(')
    t = t.replace('-', '\-')
    t = t.replace('_', '\_')
    t = t.replace('=', '\=')
    t = t.replace('.', '\.')
    return t

if __name__ == "__main__":

    verbose = False
    try:
        verbose = sys.argv[1] == '-v'
    except:
        pass

    sys.stderr = None # Avoid whiny messages about verify=False
                
    #verbose = True # Force verbose mode
    #check_folders("/foo") # Force an error
    
    check_folders("/media/photoshow/bridges")
    check_folders("/media/photoshow/waterway")
    check_folders("/media/surveys")

    urls = [
        #testing
        #"https://giscache.co.clatsop.or.us/missing",
        ("https://giscache.co.clatsop.or.us/", "cc-giscache"),
        ("https://giscache.co.clatsop.or.us/county-aerials/demo/?srs=EPSG%3A3857&format=image%2Fjpeg&wms_layer=osip2018", "cc-giscache OSIP 2018 aerial"),
        ("https://capacity.co.clatsop.or.us/cases/", "cc-giscache COVID19 cases"),
        ("https://delta.co.clatsop.or.us/apps/ClatsopCounty", "Delta CC Webmaps App"),
        ("https://delta.co.clatsop.or.us/apps/PlanningApp", "Delta Planning App"),
        ("https://delta.co.clatsop.or.us/portal", "Delta Portal"),
        ("https://delta.co.clatsop.or.us/server", "Delta Server"),
        ("http://cc-testmaps.clatsop.co.clatsop.or.us:5000", "cc-testmaps ArcGIS License Monitor"),
        ("http://cc-testmaps.clatsop.co.clatsop.or.us:3344", "cc-testmaps WABDE"),
        ("https://cc-testmaps.clatsop.co.clatsop.or.us:3001", "cc-testmaps EXB"),
        ("https://giscache.co.clatsop.or.us/photos/static", "cc-giscache Photos server"),
        ("https://echo.co.clatsop.or.us/matomo.php", "cc-giscache Matomo"),
    ]

    for url,name in urls:
        check_url(url,name)

    # All tests are done, now send a report (or not)!
    bot = telegram.Bot(token=Config.BOT_TOKEN)

    # The print statements here generate email via crontab

    my_hostname = platform.node()
    status = 0

    if len(errors)>0:
        msg = f"*Errors on {my_hostname} at {now}*\n" + errors + "\n"
        print(msg)
        rval = bot.send_message(chat_id=Config.CHAT_ID, parse_mode=mode, text=telegram_escape(msg))
        #print(rval)
        status = -1

    mode = telegram.ParseMode.MARKDOWN_V2
    if verbose and len(msg)>0:
        msg = f"*Report from {my_hostname} at {now}*\n" + msg
        print(msg)
        rval = bot.send_message(chat_id=Config.CHAT_ID, parse_mode=mode, text=telegram_escape(msg))
        #print(rval)

    exit(status)
