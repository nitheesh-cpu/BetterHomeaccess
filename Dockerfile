FROM python:3-alpine3.9

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev \
    libffi-dev openssl-dev
RUN apk add py3-pip
RUN pip3 install NumPy==1.18.0
RUN pip3 install python-dev-tools
RUN pip3 install pandas

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "/app.py" ]
