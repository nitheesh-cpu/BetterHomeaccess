FROM ubuntu:20.04

MAINTANER Nitheesh Kodarapu "nitishkoda@outlook.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "python3" , "./app.py" ]
