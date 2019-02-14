FROM trolleksii/python-base:latest

ENV WHEELHOUSE=/wheelhouse PIP_WHEEL_DIR=/wheelhouse PIP_FIND_LINKS=/wheelhouse XDG_CACHE_HOME=/cache

VOLUME /wheelhouse

VOLUME /build

VOLUME /reports

ARG USER_NAME

COPY src /app

RUN pip download -d /build -r requirements-test.txt --no-input --exists-action w && \
    pip install --no-cache-dir --no-index -f /build -r requirements-test.txt && \
    adduser -s /bin/sh -H -D $USER_NAME && \
    chown -R $USER_NAME /app

EXPOSE 8000

USER $USER_NAME

CMD ["python", "manage.py", "test" ,"--no-input"]