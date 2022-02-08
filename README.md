# dnsomatic-update

[![Docker Stars](https://img.shields.io/docker/stars/jcostom/dnsomatic-update.svg)](https://hub.docker.com/r/jcostom/dnsomatic-update/)
[![Docker Pulls](https://img.shields.io/docker/pulls/jcostom/dnsomatic-update.svg)](https://hub.docker.com/r/jcostom/dnsomatic-update/)
[![ImageLayers](https://images.microbadger.com/badges/image/jcostom/dnsomatic-update.svg)](https://microbadger.com/#/images/jcostom/dnsomatic-update)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fjcostom%2Fdnsomatic-update.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fjcostom%2Fdnsomatic-update?ref=badge_shield)

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
    -e USEIFTTT=1 \
    -e IFTTTKEY='Your IFTTT Webhook Key' \
    -e IFTTTWEBHOOK='Your IFTTT Webhook Name' \
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
| USEIFTTT | [EMPTY] | NO |
| IFTTTKEY | [EMPTY] | NO |
| IFTTTWEBHOOK | [EMPTY] | NO |  
| SITENAME | [EMPTY] | NO (YES, if USEIFTTT is true) |

On that last one - the site you're using to determine your external IP address, you've got other options you can employ as well:

* [https://api64.ipify.org/](https://api64.ipify.org/)
* [https://bot.whatismyipaddress.com/](https://bot.whatismyipaddress.com/)
* [https://myip.dnsomatic.com/](https://myip.dnsomatic.com/)

You can specify others as well, but they should return your external IP address as the only thing in the response. Pleaty of choices out there, so that stuff's up to you.

## IFTTT Usage

Create a new applet using Webhook as the "If This", then whatever is appropriate for your use case on the "Then That" side. Personally speaking, I generate a Telegram message with new IP info.

## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fjcostom%2Fdnsomatic-update.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fjcostom%2Fdnsomatic-update?ref=badge_large)
