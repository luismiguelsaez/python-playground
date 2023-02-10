FROM python:3.10-alpine

ADD requirements.txt /
RUN mkdir /app

RUN addgroup -g 1000 app && adduser -h /app -s /dev/zero -G app -D -H -u 1000 app

RUN python -m pip install -r /requirements.txt
ADD main.py /app

USER app
WORKDIR /app

ENTRYPOINT ["python", "main.py"]
