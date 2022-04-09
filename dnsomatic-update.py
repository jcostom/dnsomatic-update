#!/usr/bin/env python3

import os
import os.path
import logging
import requests
import telegram
from time import strftime, sleep

USERID = os.getenv('USERID')
PASSWORD = os.getenv('PASSWORD')
INTERVAL = os.getenv('INTERVAL', 300)
HOST = os.getenv('HOST', 'all.dnsomatic.com')
WILDCARD = os.getenv('WILDCARD', 'NOCHG')
MX = os.getenv('MX', 'NOCHG')
BACKUPMX = os.getenv('BACKUPMX', 'NOCHG')
IPADDR_SRC = os.getenv('IPADDR_SRC', 'https://ipv4.icanhazip.com/')

USETELEGRAM = int(os.getenv('USETELEGRAM', 0))
CHATID = int(os.getenv('CHATID', 0))
MYTOKEN = os.getenv('MYTOKEN', 'none')
SITENAME = os.getenv('SITENAME', 'mysite')
DEBUG = int(os.getenv('DEBUG', 0))

IPCACHE = "/config/ip.cache.txt"
VER = "3.1"
USER_AGENT = "/".join(['dnsomatic-update.py', VER])

# Setup logger
logger = logging.getLogger()
ch = logging.StreamHandler()
if DEBUG:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s',
                              datefmt='[%d %b %Y %H:%M:%S %Z]')
ch.setFormatter(formatter)
logger.addHandler(ch)


def ipChanged(ip):
    with open(IPCACHE, "r") as f:
        cachedIP = f.read()
        if cachedIP == ip:
            return False
        else:
            return True


def updateCache(ip):
    with open(IPCACHE, "w+") as f:
        f.write(ip)
    return 0


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
    logger.info('DNS-O-Matic Response: {}'.format(response.text))
    if USETELEGRAM:
        notificationText = "".join(
            ("[", SITENAME, "] WAN IP Changed @ ",
             strftime("%B %d, %Y at %H:%M. New IP == "), myIP)
        )
        sendNotification(notificationText, CHATID, MYTOKEN)


def sendNotification(msg, chat_id, token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)
    logger.info('Telegram Group Message Sent')


def main():
    while True:
        # Grab current external IP
        myIP = requests.get(IPADDR_SRC).text.rstrip('\n')

        # check to see if cache file exists and take action
        if os.path.exists(IPCACHE):
            if ipChanged(myIP):
                updateCache(myIP)
                logger.info("IP changed to {}".format(myIP))
                updateDDNS(myIP, USERID, PASSWORD)
            else:
                logger.info('No change in IP, no action taken')
        else:
            # No cache exists, create file
            updateCache(myIP)
            logger.info("No cached IP, setting to {}".format(myIP))
            updateDDNS(myIP, USERID, PASSWORD)

        sleep(INTERVAL)


if __name__ == "__main__":
    main()
