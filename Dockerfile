FROM python:3.10

ENV PYTHONBUFFERED=1
WORKDIR /django

COPY requirements.txt requirements.txt

