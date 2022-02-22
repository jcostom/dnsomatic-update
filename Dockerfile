FROM python:slim

ENV TZ=America/New_York

VOLUME "/config"

RUN pip3 install requests

RUN mkdir /app
COPY ./dnsomatic-update.py /app
RUN chmod 755 /app/dnsomatic-update.py

ENTRYPOINT [ "python3", "-u", "/app/dnsomatic-update.py" ]
