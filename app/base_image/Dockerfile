FROM python:3.12.5-bookworm

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY app/base_image/requirements.txt ./
RUN pip install -r requirements.txt

COPY common/ /app/common/