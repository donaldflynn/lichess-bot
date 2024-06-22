# Use the official Ubuntu 22.04 LTS image as the base image
FROM ubuntu:22.04 as leela-compiler
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


## Compile OpenBLAS:
RUN git clone https://github.com/xianyi/OpenBLAS.git
WORKDIR /app/OpenBLAS

# This step takes about 2 hours
RUN make TARGET=ARMV8
RUN make TARGET=ARMV8 PREFIX=/usr install

## Compile Leela

WORKDIR /app
RUN git clone https://github.com/donaldflynn/lc0.git
WORKDIR /app/lc0

RUN pip3 install --no-cache-dir meson ninja

# This step takes about 30 mins
RUN ./build.sh -Ddefault_library=static




## Compile Stockfish
# Use the official Ubuntu 22.04 LTS image as the base image
FROM ubuntu:22.04 as stockfish-compiler
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


## General build stuff
RUN apt-get -y update &&  \
    apt-get install -y \
    build-essential \
    libopenblas-dev \
    ninja-build \
    libgtest-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# https://stackoverflow.com/a/78107622
RUN rm /var/lib/dpkg/info/libc-bin.*
RUN apt-get clean
RUN apt-get update
RUN apt-get install libc-bin

RUN apt-get -y update && \
    apt-get install -y \
    curl


RUN git clone https://github.com/official-stockfish/Stockfish.git
WORKDIR /app/Stockfish/src
RUN make -j build ARCH=armv8



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

COPY --from=leela-compiler /usr /usr

WORKDIR /app/

COPY ../../requirements.txt /app/lichess-bot/requirements.txt
RUN pip3 install --no-cache-dir -r /app/lichess-bot/requirements.txt

COPY --from=stockfish-compiler /app/Stockfish/src/stockfish /app/engines/stockfish
COPY ../.. /app/
COPY --from=leela-compiler /app/lc0/build/release/lc0 /app/engines/lc0


ENTRYPOINT ["python3", "lichess-bot.py", "-v"]
