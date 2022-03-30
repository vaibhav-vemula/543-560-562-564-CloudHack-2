FROM python:3.7

RUN pip install pika tinydb requests flask

ENV PYTHONUNBUFFERED=1

WORKDIR /Users/vaibhav/Desktop/cchackathon/database

COPY database.py .

CMD [ "python", "database.py" ]