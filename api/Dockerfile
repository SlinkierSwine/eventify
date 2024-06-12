FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /src
COPY requirements.txt ./
RUN apt-get update
RUN pip install -r requirements.txt --no-cache-dir --no-input
COPY . /src/
