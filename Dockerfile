FROM alpine:latest

VOLUME "/config"

RUN \
    apk add --no-cache py3-requests \
    && rm -rf /var/cache/apk/*

RUN mkdir /app
COPY ./dnsomatic-update.py /app
RUN chmod 755 /app/dnsomatic-update.py

ENTRYPOINT [ "/app/dnsomatic-update.py" ]