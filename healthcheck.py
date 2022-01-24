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
    t = 8 
    url_escaped = url.replace(')', '\)')
    name = name.replace('-', '\-')
    try:
        r = requests.get(url, timeout=t, verify=False)
        if r.status_code == 200: 
            msg += "%s [%s](%s)\n" % (str(r.elapsed).replace('.', '\.'), name, url_escaped)
            return 0
        errors += "Status code %s on [%s](%s)\n" % (r.status_code, name, url_escaped)

    except requests.exceptions.Timeout:
        errors += "Timeout on [%s](%s)\n" % (name, url_escaped)
    except requests.exceptions.ConnectionError:
        errors += "Connection failed [%s](%s)\n" % (name, url_escaped)


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
        ("https://giscache.co.clatsop.or.us/photoshow", "cc-giscache Photoshow"),
        ("https://webforms.co.clatsop.or.us", "cc-giscache WebHooks"),
    ]

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

