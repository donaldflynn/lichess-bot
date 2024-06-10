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


## Leela chess stuff
RUN apt-get -y update &&  \
    apt-get install -y \
    build-essential \
    libopenblas-dev \
    ninja-build \
    libgtest-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/xianyi/OpenBLAS.git
WORKDIR /app/OpenBLAS

# This step takes about 2 hours
RUN make TARGET=ARMV8
RUN make TARGET=ARMV8 PREFIX=/usr install

WORKDIR /app
RUN git clone https://github.com/donaldflynn/lc0.git
WORKDIR /app/lc0

RUN pip3 install --no-cache-dir meson ninja

# This step takes about 30 mins
RUN ./build.sh -Ddefault_library=static

COPY requirements.txt /app/lichess-bot/requirements.txt
RUN pip3 install --no-cache-dir -r /app/lichess-bot/requirements.txt

COPY . /app/

RUN mv /app/lc0/build/release/lc0 /app/engines

WORKDIR /app/
ENTRYPOINT ["python3", "lichess-bot.py", "-v"]
