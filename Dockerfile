from python:3.7-alpine
MAINTAINER MITH
# RUN echo -e http://mirrors.ustc.edu.cn/alpine/v3.7/main/ > /etc/apk/repositories
# RUN echo -e https://hub-mirror.c.163.com/alpine/v3.7/main/ > /etc/apk/repositories
RUN cat /etc/apk/repositories

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# RUN apk update
RUN apk add --update postgresql-client jpeg-dev
RUN apk add --update --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# RUN apk add postgresql-dev

RUN pip install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user