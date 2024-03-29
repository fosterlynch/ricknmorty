FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    gcc \
    g++ \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3.10-distutils \
    python3-pip

RUN pip3 install requests python-dotenv
RUN pip3 install notebook mortgage matplotlib
RUN pip3 install pytest
WORKDIR ./proj

COPY .env ./
COPY /databases ./
COPY ./src .
COPY devurls.json ./

COPY ./tests ./tests
RUN python3 -m pytest -cov . -vv