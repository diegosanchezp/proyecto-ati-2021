FROM ubuntu:latest
WORKDIR /app
COPY . ./
# Install dependencies and compile files
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.9 python3-pip && \
    pip3 install --no-deps -r requirements.txt
# run the software contained in your image
CMD ["python3","run.py"]
