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

RUN pip3 install requests beautifulsoup4 python-dotenv
RUN pip3 install notebook mortgage matplotlib
RUN pip3 install pytest

WORKDIR ./explore
COPY .env ./
COPY mortgage.ipynb ./
COPY testme.py ./
COPY realestate.py ./
COPY api.py ./
COPY taxrates.sqlite ./
COPY taxes.py ./
COPY retry.sqlite ./
# COPY tests/ tests/
# RUN python3 -m pytest tests