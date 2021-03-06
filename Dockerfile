FROM python:3.9-alpine3.13
LABEL maintainer="jjbeekman"

ENV PYTHONUNBUFFERED 1
ARG DEV=false
ENV PATH="/py/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then pip install -r /tmp/requirements.dev.txt; fi &&\
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home fashion-cloud-user

COPY app /app
WORKDIR /app

USER fashion-cloud-user