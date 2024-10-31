FROM python:3.11

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ENV PYTHONPATH /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app