FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /home/django/

COPY requirements.txt requirements.txt

RUN ls -l /

RUN apt update && apt install build-essential -y

RUN pip install -r requirements.txt


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8010"]