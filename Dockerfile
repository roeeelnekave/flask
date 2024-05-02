FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask prometheus-flask-exporter

EXPOSE 5005

ENV FLASK_APP=index.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5005"]