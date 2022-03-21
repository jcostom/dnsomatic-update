# dnsomatic-update

Lightweight DNS-o-Matic Updater in Python.

Why build this? I was having problems with ddclient properly updating DNS-O-Matic, and wanted to rebuild it in Python and containerize the script. Now with automatic vulnerability scanning from Docker Hub integrated!

So, how to use this beast? It's rather simple, really.

## Pull the image

`docker pull jcostom/dnsomatic-update`

## Run the container

For example, if you're content to use the defaults, only specifying username & password:

```bash
docker run -d \
    --name=dnsomatic \
    --restart=unless-stopped \
    --user=1000:1000 \
    -e USERID='YOUR-DNSOMATIC-USERNAME' \
    -e PASSWORD='YOUR-DNSOMATIC-PASSWORD' \
    -e USETELEGRAM=1 \
    -e CHATID='Your Telegram Chat ID' \
    -e MYTOKEN='Your Telegram Bot Token' \
    -e SITENAME='Home' \
    -e TZ='America/New_York' \
    jcostom/dnsomatic-update
```

If you'd like to more easily view the IP cached by the script, mount a directory as /config inside the container. For example, add `-v /var/docks/dnsomatic:/config` to your container invocation. The `--user UID:GID` parameter in starting the container is highly recommended. No point in running the container as root if you don't need to, right? If you do this and map a volume to the local filesystem, just make sure the UID:GID combo has write permission to that directory, otherwise, your IP cache will never be written.

## Available parameters

Pass the following parameters to the container as environment variables (-e switch).

| Variable | Default Value | Required to Launch? |
|---|---|---|
| USERID | [EMPTY] | YES! |
| PASSWORD | [EMPTY] | YES! |
| INTERVAL (in seconds) | 300 | NO |
| HOST | all.dnsomatic.com | NO |
| WILDCARD | [EMPTY] | NO |
| MX | [EMPTY] | NO |
| BACKUPMX | [EMPTY] | NO |
| IPADDR_SRC | [https://ipv4.icanhazip.com/](https://ipv4.icanhazip.com/) | NO |
| USETELEGRAM | [EMPTY] | NO |
| CHATID | [EMPTY] | NO (YES, if USETELEGRAM is true) |
| MYTOKEN | [EMPTY] | NO (YES, if USETELEGRAM is true) |  
| SITENAME | [EMPTY] | NO (YES, if USETELEGRAM is true) |

On that last one - the site you're using to determine your external IP address, you've got other options you can employ as well:

* [https://api64.ipify.org/](https://api64.ipify.org/)
* [https://bot.whatismyipaddress.com/](https://bot.whatismyipaddress.com/)
* [https://myip.dnsomatic.com/](https://myip.dnsomatic.com/)

You can specify others as well, but they should return your external IP address as the only thing in the response. Pleaty of choices out there, so that stuff's up to you.

## Telegram Usage

Create a Telegram Bot in the usual manner, setup a group or secret chat, find the chat id and plug the appropriate values in here if you'd like to use that. There are loads of guides online that tell you how to do that, so I won't repeat that "howto" here.
