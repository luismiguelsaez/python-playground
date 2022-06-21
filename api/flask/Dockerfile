FROM python:3.8-alpine

RUN addgroup app && adduser -s /bin/false -D -G app app
RUN mkdir /app

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD code/ /app/
RUN chown -R app.app /app

USER app

ENTRYPOINT [ "python" ]
CMD [ "/app/main.py" ]
