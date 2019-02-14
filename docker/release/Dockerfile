FROM trolleksii/python-base:latest

COPY ./target /wheelhouse

RUN pip install --no-index -f /wheelhouse todolistapi && \
    rm -rf /wheelhouse

EXPOSE 8000

CMD ["gunicorn", "-w 2", "--bind 0.0.0.0:8000", "todolistapi.wsgi:application"]
