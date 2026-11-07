FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir "pika>=1.3"
COPY consumer_rabbit.py .
CMD ["python", "-u", "consumer_rabbit.py"]
