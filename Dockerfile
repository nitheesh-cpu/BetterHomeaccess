FROM ubuntu:20.04
RUN apt-get install \
    python3 python3-dev gcc \
    gfortran musl-dev \
    libffi-dev openssl-dev python3-pip


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "/app.py" ]
