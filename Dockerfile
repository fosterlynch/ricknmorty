FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

# Temporarily granting root access
USER root

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

RUN pip3 install notebook mortgage matplotlib

COPY houseprices.ipynb ./


