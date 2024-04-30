FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /code/backend/

RUN pip install --upgrade pip
COPY ./backend/requirements.txt /code/backend/
RUN pip install -r requirements.txt


COPY ./backend /code/backend/
