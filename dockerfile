FROM python:3.10-slim

RUN mkdir -p /app

COPY /model /app/