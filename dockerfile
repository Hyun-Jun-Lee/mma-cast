FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

COPY ./app /app

WORKDIR /app

# Install dependencies
RUN python -m venv /app/py && \
    /app/py/bin/pip install --upgrade pip && \
    apt-get clean -y && \
    apt-get update -y

RUN /app/py/bin/pip install -r requirements.txt

# Expose port
EXPOSE 8000


# Set the entry point command to start your FastAPI application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
