FROM python:slim

ARG BUILD_DATE
ARG VCS_REF

ENV TZ=America/New_York

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="https://github.com/jcostom/dnsomatic-update.git" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.schema-version="1.0.0"

VOLUME "/config"

RUN \
    apt update \
    && apt -yq install python3-requests 

RUN mkdir /app
COPY ./dnsomatic-update.py /app
RUN chmod 755 /app/dnsomatic-update.py

ENTRYPOINT [ "python3", "-u", "/app/dnsomatic-update.py" ]
