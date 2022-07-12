FROM python:3.8.2-alpine
RUN apk --no-cache add musl-dev linux-headers g++
RUN pip3 install --upgrade pip setuptools wheel
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
