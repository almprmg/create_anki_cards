# filepath: /home/bh/py_projact/create_anki_cards/user-service/Dockerfile
FROM python:3.12-slim-bullseye

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    pkg-config \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt --verbose
COPY . /app

EXPOSE 5000