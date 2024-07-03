FROM ubuntu:latest
LABEL authors="remag29"

RUN apt-get update && apt-get install -y python3.12 python3.12-dev

RUN pip install -r requirements.txt
