FROM python:3.10.5-slim
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential
RUN rm -rf /var/lib/apt/lists/*
COPY ./Requirements/* /tmp/Requirements/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/Requirements/local.txt
RUN rm -r -f /tmp/Requirements
RUN mkdir -p /App/
COPY ./Apps /App/Apps
COPY ./Project /App/Project
COPY ./manage.py /App/
WORKDIR /App
