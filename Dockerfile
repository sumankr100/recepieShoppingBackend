FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /recepieShoppingBackend
COPY models /recepieShoppingBackend/models
COPY resources /recepieShoppingBackend/resources
COPY app.py db.py security.py ./recepieShoppingBackend/
WORKDIR /recepieShoppingBackend
