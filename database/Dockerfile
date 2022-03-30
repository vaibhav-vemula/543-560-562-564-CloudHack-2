# basic python image
FROM python:3.7

# install pika to access rabbitmq
RUN pip install pika
RUN pip install tinydb
RUN pip install requests
RUN pip install flask

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1

# declare the source directory
WORKDIR /Users/vaibhav/Desktop/cchackathon/database

# copy the file
COPY database.py .

# start command
CMD [ "python", "database.py" ]