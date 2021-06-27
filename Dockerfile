FROM python:3.9.5-alpine3.13
WORKDIR /app
COPY . ./

# Install dependencies and compile files
RUN apk add --no-cache \
    musl-dev build-base gcc py-cryptography libffi-dev openssl-dev cargo make \
    npm \
    && npm install && npm run build && \
    pip3 install -r requirements.txt --no-deps
# run the software contained in your image
CMD ["python3","run.py"]
