FROM ubuntu:latest
WORKDIR /app
COPY . ./
# Install dependencies and compile files
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.9 python3-pip curl && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    pip3 install --no-deps -r requirements.txt && \
    npm install

# run the software contained in your image
CMD ["python3","run.py"]
