FROM alpine:latest

RUN apk add --no-cache python3-dev
RUN apk add py3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "/app.py" ]
