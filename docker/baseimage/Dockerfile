FROM python:3.7-alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python -m pip install psycopg2 && \
    apk --purge del .build-deps
