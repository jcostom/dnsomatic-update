#!/usr/bin/env python3

import os
import os.path
import requests
import time

USERID = os.getenv('USERID')
PASSWORD = os.getenv('PASSWORD')
INTERVAL = os.getenv('INTERVAL', 300)
HOST = os.getenv('HOST', 'all.dnsomatic.com')
WILDCARD = os.getenv('WILDCARD', 'NOCHG')
MX = os.getenv('MX', 'NOCHG')
BACKUPMX = os.getenv('BACKUPMX', 'NOCHG')
IPADDR_SRC = os.getenv('IPADDR_SRC', 'https://ipv4.icanhazip.com/')
IPCACHE = "/config/ip.cache.txt"
# IPCACHE = "ip.cache.txt"

USEIFTTT = os.getenv('USEIFTTT')
IFTTTKEY = os.getenv('IFTTTKEY')
IFTTTWEBHOOK = os.getenv('IFTTTWEBHOOK')

VER = 'dnsomatic-update.py v0.9.4-fmf'

def ipChanged(myIP):
    f = open(IPCACHE,"r")
    cachedIP = f.readline()
    f.close()
    if cachedIP == myIP:
        return False
    else:
        return True

def updateCache(myIP):
    f = open(IPCACHE,"w+")
    f.write(myIP)
    f.close()

def updateDDNS(myIP, user, passwd):
    updateURL = "&".join(
        ( "https://updates.dnsomatic.com/nic/update?hostname={}".format(HOST),
          "myip={}".format(myIP),
          "wildcard={}".format(WILDCARD),
          "mx={}".format(MX),
          "backmx={}".format(BACKUPMX))
        )

    headers = {'User-Agent': VER }
    response = requests.get(updateURL, headers=headers, auth=(user, passwd))
    print(time.strftime("[%d %b %Y %H:%M:%S %Z]", time.localtime()) + " DNS-O-Matic Response: {}".format(response.text))
    if USEIFTTT:
        triggerWebHook(myIP)

def triggerWebHook(newIP):
    webHookURL = "/".join(
        ("https://maker.ifttt.com/trigger",
        IFTTTWEBHOOK,
        "with/key",
        IFTTTKEY)
    )
    headers = {'User-Agent': VER }
    payload = { 'value1': newIP }
    response = requests.post(webHookURL, headers=headers, data=payload)
    print(time.strftime("[%d %b %Y %H:%M:%S %Z]", time.localtime()) + " IFTTT Response: {}".format(response.text))

def main():
    while True:
        # Grab current external IP
        myIP = requests.get(IPADDR_SRC).text.rstrip('\n')

        # check to see if cache file exists and take action
        if os.path.exists(IPCACHE):
            if ipChanged(myIP):
                updateCache(myIP)
                print("IP changed to {}".format(myIP))
                updateDDNS(myIP, USERID, PASSWORD)
            else:
                print(time.strftime("[%d %b %Y %H:%M:%S %Z]", time.localtime()) + " No change in IP, no action taken.")  
        else:
            # No cache exists, create file
            updateCache(myIP)
            print(time.strftime("[%d %b %Y %H:%M:%S %Z]", time.localtime()) + " No cached IP, setting to {}".format(myIP))
            updateDDNS(myIP, USERID, PASSWORD)

        time.sleep(INTERVAL)
    
if __name__ == "__main__":
    main()
