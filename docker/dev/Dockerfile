FROM trolleksii/python-base:latest

ARG USER_NAME

COPY src /app

RUN pip download -d /build -r requirements-test.txt --no-input --exists-action w && \
    pip install --no-cache-dir --no-index -f /build -r requirements-test.txt && \
    adduser -s /bin/sh -H -D $USER_NAME && \
    chown -R $USER_NAME /app

EXPOSE 8000

USER $USER_NAME

CMD ["python", "manage.py", "test" ,"--no-input"]