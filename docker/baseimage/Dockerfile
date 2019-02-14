FROM python:3.7-alpine

ENV WHEELHOUSE=/wheelhouse PIP_WHEEL_DIR=/wheelhouse PIP_FIND_LINKS=/wheelhouse XDG_CACHE_HOME=/cache

VOLUME /wheelhouse

VOLUME /build

VOLUME /reports

WORKDIR /app

RUN apk update && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python -m pip install psycopg2 && \
    apk --purge del .build-deps
