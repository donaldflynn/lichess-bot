# Use the official Ubuntu 22.04 LTS image as the base image
FROM nvidia/cuda:12.5.0-runtime-ubuntu22.04
ARG DEBIAN_FRONTEND=noninteractive

# Install essential packages
RUN apt-get -y update && \
    apt-get install -y \
    python3 \
    python3-pip \
    nano \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir meson ninja

WORKDIR /app
RUN git clone https://github.com/donaldflynn/lc0.git
WORKDIR /app/lc0

RUN ./build.sh

COPY ../../requirements.txt /app/lichess-bot/requirements.txt
RUN pip3 install --no-cache-dir -r /app/lichess-bot/requirements.txt

COPY ../.. /app/

RUN mv /app/lc0/build/release/lc0 /app/engines

WORKDIR /app/
ENTRYPOINT ["python3", "lichess-bot.py", "-v"]
