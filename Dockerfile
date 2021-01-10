from python:3.7-alpine
MAINTAINER MITH
# RUN echo -e http://mirrors.ustc.edu.cn/alpine/v3.7/main/ > /etc/apk/repositories
# RUN echo -e https://hub-mirror.c.163.com/alpine/v3.7/main/ > /etc/apk/repositories
RUN cat /etc/apk/repositories

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk update
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user