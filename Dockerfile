FROM python:3.8.5-alpine

RUN apk update \
    && apk add --no-cache --virtual build-dependencies build-base gcc wget git cmake \
    && apk add --no-cache taglib taglib-dev \
    && pip install pytaglib \
    && apk del build-dependencies

WORKDIR /code
RUN git clone https://github.com/sam016/Songs-Dup/ /code/

