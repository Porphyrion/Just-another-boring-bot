# syntax=docker/dockerfile:1

FROM python:3.8-slim

RUN mkdir -p /user/src/024bot
WORKDIR /usr/src/024bot
COPY . .
RUN apt-get update && apt install install tesseract-ocr
RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["python3", "main.py"]
