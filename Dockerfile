FROM python:3.11

RUN mkdir /insurance_api

WORKDIR /insurance_api

COPY . .

RUN pip install -r requirements.txt
