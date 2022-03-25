#!/usr/bin/env python3

import os
import os.path
import requests
import telegram
import time

USERID = os.getenv('USERID')
PASSWORD = os.getenv('PASSWORD')
INTERVAL = os.getenv('INTERVAL', 300)
HOST = os.getenv('HOST', 'all.dnsomatic.com')
WILDCARD = os.getenv('WILDCARD', 'NOCHG')
MX = os.getenv('MX', 'NOCHG')
BACKUPMX = os.getenv('BACKUPMX', 'NOCHG')
IPADDR_SRC = os.getenv('IPADDR_SRC', 'https://ipv4.icanhazip.com/')

USETELEGRAM = os.getenv('USETELEGRAM', 0)
CHATID = int(os.getenv('CHATID', 0))
MYTOKEN = os.getenv('MYTOKEN', 'none')
SITENAME = os.getenv('SITENAME', 'mysite')

IPCACHE = "/config/ip.cache.txt"
# IPCACHE = "ip.cache.txt"
VER = "3.0.1"
USER_AGENT = "dnsomatic-update.py/" + VER


def ipChanged(myIP):
    f = open(IPCACHE, "r")
    cachedIP = f.readline()
    f.close()
    if cachedIP == myIP:
        return False
    else:
        return True


def updateCache(myIP):
    f = open(IPCACHE, "w+")
    f.write(myIP)
    f.close()


def updateDDNS(myIP, user, passwd):
    updateURL = "&".join(
        ("https://updates.dnsomatic.com/nic/update?hostname={}".format(HOST),
         "myip={}".format(myIP),
         "wildcard={}".format(WILDCARD),
         "mx={}".format(MX),
         "backmx={}".format(BACKUPMX))
        )

    headers = {'User-Agent': USER_AGENT}
    response = requests.get(updateURL, headers=headers, auth=(user, passwd))
    writeLogEntry('DNS-O-Matic Response', response.text)
    if USETELEGRAM == "1":
        notificationText = "".join(
            ("[", SITENAME, "] WAN IP Changed @ ",
             time.strftime("%B %d, %Y at %H:%M. New IP == "), myIP)
        )
        sendNotification(notificationText, CHATID, MYTOKEN)


def sendNotification(msg, chat_id, token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)
    writeLogEntry("Telegram Group Message Sent", "")


def writeLogEntry(message, status):
    print(time.strftime("[%d %b %Y %H:%M:%S %Z]",
          time.localtime()) + " {}: {}".format(message, status))


def main():
    while True:
        # Grab current external IP
        myIP = requests.get(IPADDR_SRC).text.rstrip('\n')

        # check to see if cache file exists and take action
        if os.path.exists(IPCACHE):
            if ipChanged(myIP):
                updateCache(myIP)
                writeLogEntry('IP changed to', myIP)
                updateDDNS(myIP, USERID, PASSWORD)
            else:
                writeLogEntry('No change in IP, no action taken', '')
        else:
            # No cache exists, create file
            updateCache(myIP)
            writeLogEntry('No cached IP, setting to', myIP)
            updateDDNS(myIP, USERID, PASSWORD)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
