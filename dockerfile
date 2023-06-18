FROM python:3.9-slim-buster

# Create a non-root user
# RUN groupadd -r fastuser && useradd -r -g fastuser fastuser

# Set the working directory and ownership to the non-root user
WORKDIR /app
# RUN chown -R fastuser:fastuser /app

# Switch to the non-root user
# USER fastuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Copy requirements and application code
# COPY --chown=fastuser:fastuser ./requirements.txt /tmp/requirements.txt
# COPY --chown=fastuser:fastuser ./app /app
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app


# Install dependencies
RUN python -m venv /app/py && \
    /app/py/bin/pip install --upgrade pip && \
    apt-get clean -y && \
    apt-get update -y && \
    /app/py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

# Expose port
EXPOSE 8000


# Set the entry point command to start your FastAPI application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
