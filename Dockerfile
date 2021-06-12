FROM alpine:3.13
RUN apk add py3-pip
RUN pip3 install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD ["python3","src/app.py"]