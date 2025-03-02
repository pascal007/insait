FROM python:3.11-bookworm
LABEL authors="Pascal Ezeama"

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN  apt-get update

RUN apt-get install build-essential


COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . .

