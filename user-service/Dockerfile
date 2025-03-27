
FROM python:3.12-slim-bullseye

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev pkg-config \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt --verbose
COPY . /app

EXPOSE 5000



ENV FLASK_APP=run.py
ENV FLASK_ENV=development


