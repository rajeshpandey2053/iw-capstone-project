# pull official base image
FROM python:3.8.2-alpine

# set work directory
RUN mkdir /iw-acad-hamro-note-be
WORKDIR /iw-acad-hamro-note-be

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --upgrade Pillow
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN adduser -D user
USER user
