FROM amd64/python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

COPY ./app /app

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && \
    apt-get clean -y && \
    apt-get update -y && \
    apt-get install -y pkg-config libpq-dev libmariadb-dev build-essential && \
    pip install -r /app/requirements.txt

# Expose port
EXPOSE 8000
