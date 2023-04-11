FROM python:3.8.10-slim

ENV TZ=Asia/Shanghai

COPY ./sources.list /etc/apt/sources.list

RUN echo "${TZ}" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime && \
    apt update && \
    apt install -y  \
        gcc \
        g++ \
        libssl-dev  \
        libffi-dev \
        libbz2-dev \
        build-essential \
        python3-dev \
        libffi-dev \
        openssl \
        default-libmysqlclient-dev \
        supervisor && \
    apt clean && \
    apt autoremove --purge && \
    rm -rf /tmp/* && \
    rm -rf /var/lib/apt/lists/*
