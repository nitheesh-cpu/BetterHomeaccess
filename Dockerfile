FROM python:3.8.2-alpine
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
