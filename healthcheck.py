#!/usr/bin/env -S conda run -n telegram --no-capture-output python
import sys
import os
import platform
from glob import glob
import requests
from requests.sessions import merge_setting
import telegram
from config import Config

msg = ""
errors = ""

def check_folders(path):
    """
    Check volumes are mounted by looking for files in each one.
    
    There are currently 3 folders mounted via CIFS from /etc/fstab
    and there have to be a few files in each of them.
    """
    global msg, errors

    # These are mount points for folders on cc-files server,
    # the mount points always exist but have files in them if they are
    # working correctly.
    folders = glob(path + "/*")
    if len(folders)==0:
        errors += "Mount point missing \"%s\"\n" % path
        return 1

    msg += "Mount point \"%s\"\n" % path

    for folder in folders:
        try:
            count = len(glob(os.path.join(folder, "*")))
            if count: 
                msg += "\"%s\" has %d files GOOD\n" % (folder, count)
                continue
        except Exception as e:
            errors += str(e)
        errors += "Folder is not mounted, \"%s\"\n" % folder
        
    msg += "\n"


def check_url(url,name):
    """
    Make sure there is a web server running.
    """
    global msg, errors

    # Note, you can set timeout to .001 to test timeouts.
    # Normally it should be high enough to accomodate slow services
    # such as the map proxy.
    t = 8 
    escaped = url.replace(')', '\)')
    try:
        r = requests.get(url, timeout=t)
        if r.status_code == 200: 
            msg += "%s [%s](%s)\n" % (str(r.elapsed).replace('.', '\.'), name, escaped)
            return 0
        errors += "Status code %s on [%s](%s)\n" % (r.status_code, name, escaped)
    except requests.exceptions.Timeout:
        errors += "Timeout on [%s](%s)\n" % (name, escaped)
    except requests.exceptions.ConnectionError:
        errors += "Connection failed [%s](%s)\n" % (name, escaped)


if __name__ == "__main__":

    try:
        verbose = sys.argv[1] == '-v'
    except:
        verbose = False
            
    #verbose = True # Force verbose mode
    #check_folders("/foo") # Force an error
    
    check_folders("/media/photoshow")

    urls = [
        #testing
        #"https://giscache.co.clatsop.or.us/missing",
        ("https://giscache.co.clatsop.or.us/", "GISCache"),
        ("https://giscache.co.clatsop.or.us/county-aerials/demo/?srs=EPSG%3A3857&format=image%2Fjpeg&wms_layer=osip2018", "OSIP 2018 aerial"),
        ("https://capacity.co.clatsop.or.us/cases/", "COVID19 cases"),
        ("https://delta.co.clatsop.or.us/apps/ClatsopCounty", "CC Webmaps App"),
        ("https://delta.co.clatsop.or.us/apps/PlanningApp", "CC Planning App"),
        ("https://delta.co.clatsop.or.us/portal", "Delta Portal"),
        ("https://delta.co.clatsop.or.us/server", "Delta Server"),
        ("http://cc-testmaps.clatsop.co.clatsop.or.us:5000", "ArcGIS License Monitor"),
        ("https://giscache.co.clatsop.or.us/photoshow", "Photoshow"),
    ]
    msg += "Web services\n"
    for url,name in urls:
        check_url(url,name)

    # All tests are done, now send a report (or not)!
    bot = telegram.Bot(token=Config.BOT_TOKEN)

    # The print statements here generate email via crontab

    hostname = platform.node().replace('-','\-')

    mode = telegram.ParseMode.MARKDOWN_V2
    if verbose and len(msg)>0:
        msg = "*Report from " + hostname + "*\n" + msg
        print(msg)
        rval = bot.send_message(chat_id=Config.CHAT_ID, parse_mode=mode, text=msg)
        #print(rval)
    
    if len(errors)>0:
        errors = "*ERRORS on " + hostname + "*\n" + errors
        print(errors)
        rval = bot.send_message(chat_id=Config.CHAT_ID, parse_mode=mode, text=errors)
        #print(rval)

    exit(0)

