FROM python:3.9.2-slim
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app