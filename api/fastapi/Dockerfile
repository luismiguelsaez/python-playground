FROM python:3.11-alpine

RUN mkdir /app
RUN addgroup -g 1000 app && adduser -h /app -s /dev/null -u 1000 -G app -D app

ADD requirements.txt /
RUN pip install -r /requirements.txt
ADD src/ app/

WORKDIR /app
USER app

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
