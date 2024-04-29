FROM python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY index.py .

EXPOSE 5005

CMD ["python", "index.py"]