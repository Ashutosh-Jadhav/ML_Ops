FROM python:3.10-slim

RUN mkdir -p /app/model

COPY model /app/model/