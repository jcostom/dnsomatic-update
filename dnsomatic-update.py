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
VER = "3.4"
USER_AGENT = f"dnsomatic-update.py/{VER}"

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


def ip_changed(ip: str) -> bool:
    with open(IPCACHE, "r") as f:
        cached_ip = f.read()
        if cached_ip == ip:
            return False
        else:
            return True


def update_cache(ip: str) -> int:
    with open(IPCACHE, "w+") as f:
        f.write(ip)
    return 0


def send_notification(msg: str, chat_id: int, token: str) -> None:
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)
    logger.info('Telegram Group Message Sent')


def send_update(ip: str, user: str, passwd: str) -> None:
    update_url = "&".join(
        [f"https://updates.dnsomatic.com/nic/update?hostname={HOST}",
         f"myip={ip}",
         f"wildcard={WILDCARD}",
         f"mx={MX}",
         f"backmx={BACKUPMX}"]
        )

    headers = {'User-Agent': USER_AGENT}
    response = requests.get(update_url, headers=headers, auth=(user, passwd))
    logger.info(f"DNS-O-Matic Response: {response.text}")
    if USETELEGRAM:
        notification_text = "".join(
            ("[", SITENAME, "] WAN IP Changed @ ",
             strftime("%B %d, %Y at %H:%M. New IP == "), ip)
        )
        send_notification(notification_text, CHATID, MYTOKEN)


def main():
    while True:
        # Grab current external IP
        current_ip = requests.get(IPADDR_SRC).text.rstrip('\n')

        # check to see if cache file exists and take action
        if os.path.exists(IPCACHE):
            if ip_changed(current_ip):
                update_cache(current_ip)
                logger.info(f"IP changed to {current_ip}")
                send_update(current_ip, USERID, PASSWORD)
            else:
                logger.info('No change in IP, no action taken')
        else:
            # No cache exists, create file
            update_cache(current_ip)
            logger.info(f"No cached IP, setting to {current_ip}")
            send_update(current_ip, USERID, PASSWORD)

        sleep(INTERVAL)


if __name__ == "__main__":
    main()
