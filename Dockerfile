FROM python:3.11.3-slim-bullseye

ARG TZ=America/New_York

VOLUME "/config"

RUN \
    pip install requests \
    && pip install python-telegram-bot \
    && pip cache purge

RUN mkdir /app
COPY ./dnsomatic-update.py /app
RUN chmod 755 /app/dnsomatic-update.py

ENTRYPOINT [ "python3", "-u", "/app/dnsomatic-update.py" ]
