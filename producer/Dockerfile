FROM python:3.7

RUN pip install pika requests flask

ENV PYTHONUNBUFFERED=1

WORKDIR /Users/vaibhav/Desktop/cchackathon/producer

COPY producer.py .

EXPOSE 8000

CMD [ "python", "producer.py"]