FROM python:3.12
LABEL authors="remag29"

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./app /app

CMD ["python", "/app/main.py"]
