FROM python:3.9.5-alpine3.13
WORKDIR /app
COPY . ./
ENV PACKAGES="gcc musl-dev python3-dev libffi-dev openssl-dev cargo"
# Install dependencies and compile files
RUN apk add --no-cache $PACKAGES npm && \
    pip3 install -r requirements.txt --no-deps && \
    npm install && \
    apk del --purge $PACKAGES
# run the software contained in your image
CMD ["python3","run.py"]
