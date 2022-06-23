FROM python:3.10.5
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

WORKDIR /
COPY . /
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN /usr/local/bin/python -m pip install -r /Requirements/local.txt
