FROM trolleksii/python-base:latest

ENV WHEELHOUSE=/wheelhouse PIP_WHEEL_DIR=/wheelhouse PIP_FIND_LINKS=/wheelhouse XDG_CACHE_HOME=/cache

VOLUME /wheelhouse

VOLUME /build

VOLUME /reports

ARG USER_NAME

COPY src/requirements.txt /app/requirements.txt

COPY src/requirements-test.txt /app/requirements-test.txt

COPY src/manage.py /app/manage.py

COPY src/setup.py /app/setup.py

RUN pip download -d /build -r requirements-test.txt --no-input --exists-action w && \
    pip install --no-cache-dir --no-index -f /build -r requirements-test.txt && \
    adduser -s /bin/sh -H -D $USER_NAME && \
    chown -R $USER_NAME /app && \
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz

EXPOSE 8000

USER $USER_NAME

CMD ["python", "manage.py", "test" ,"--no-input"]