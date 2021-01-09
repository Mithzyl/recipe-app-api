from python:3.7-alpine
MAINTAINER MITH

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user