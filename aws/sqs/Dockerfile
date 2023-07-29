FROM python:3.11-alpine

RUN apk update && apk add --no-cache bash

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

ADD sns.py /app/sns.py
ADD sqs.py /app/sqs.py
ADD entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN chown -R app:app /app
USER app

ENTRYPOINT [ "/app/entrypoint.sh" ]
