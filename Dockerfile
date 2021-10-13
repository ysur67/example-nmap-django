# syntax=docker/dockerfile:1
FROM python:3.9.6
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y nmap
COPY . /code/
COPY ./entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
