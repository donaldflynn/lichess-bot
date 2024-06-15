# Use the official Ubuntu 22.04 LTS image as the base image
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install essential packages
RUN apt-get -y update && \
    apt-get install -y \
    python3 \
    python3-pip \
    nano \
    && rm -rf /var/lib/apt/lists/*

COPY ../../requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/lichess-bot/requirements.txt

COPY ../../requirements.dev.txt /app/requirements.dev.txt
RUN pip3 install --no-cache-dir -r /app/lichess-bot/requirements.dev.txt
