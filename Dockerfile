FROM python:3.9.5-alpine3.13
WORKDIR /app
COPY . .
# Install dependencies and compile files
RUN apk add --no-cache npm && npm install && npm run build && \
    pip3 install -r requirements.txt
# run the software contained in your image
CMD ["python3","run.py"]
