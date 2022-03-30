FROM python:3.7

RUN pip install pika requests flask

ENV PYTHONUNBUFFERED=1

WORKDIR /Users/vaibhav/Desktop/cchackathon/consumer

COPY consumer.py .

CMD [ "python", "consumer.py" ]