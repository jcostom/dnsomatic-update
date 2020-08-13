#!/usr/bin/env python3

import os
import os.path
import requests
import time

USERID = os.getenv('USERID')
PASSWORD = os.getenv('PASSWORD')
INTERVAL = os.getenv('INTERVAL', 3600)
HOST = os.getenv('HOST', 'all.dnsomatic.com')
WILDCARD = os.getenv('WILDCARD', 'NOCHG')
MX = os.getenv('MX', 'NOCHG')
BACKUPMX = os.getenv('BACKUPMX', 'NOCHG')
IPADDR_SRC = os.getenv('IPADDR_SRC', 'https://ipv4.icanhazip.com/')
IPCACHE = "/config/ip.cache.txt"

def constructURL(myip):
    return "&".join(
        ("https://updates.dnsomatic.com/nic/update?hostname={}".format(HOST),
        "myip={}".format(myip),
        "wildcard={}".format(WILDCARD),
        "mx={}".format(MX),
        "backmx={}".format(BACKUPMX))
    )

def updateDDNS(updateURL, user, passwd):
    headers = {'User-Agent': 'dnsomatic-update.py v0.1'}
    response = requests.get(updateURL, headers=headers, auth=(user, passwd))
    print(response.text)

def main():
    while True:
        # Grab current external IP
        myip = requests.get(IPADDR_SRC).text.rstrip('\n')

        # check to see if cache file exists and take action
        if os.path.exists(IPCACHE):
            f = open(IPCACHE,"r")
            cachedIP = f.readline()
            f.close()

            if cachedIP == myip:
                print("No change in IP")
            else:
                # IP changed, Construct Update URL
                updateURL = constructURL(myip)
                print("IP changed {}".format(updateURL))
                updateDDNS(updateURL, USERID, PASSWORD)
        else:
            # No cache exists, create file
            f = open(IPCACHE,"w+")
            f.write(myip)
            f.close()

            # Construct Update URL
            updateURL = constructURL(myip)
            print("No cached IP {}".format(updateURL))
            updateDDNS(updateURL, USERID, PASSWORD)

        time.sleep(INTERVAL)
    
if __name__ == "__main__":
    main()
