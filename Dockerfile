# Base image for Python
FROM python:3.11-slim

# Set environment variables to prevent interactive prompts and configure Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt /app/

# Install system dependencies and Python dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the entire project into the container
COPY . /app/

# Set up Scrapy logs folder
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=llm_django.settings
ENV PYTHONPATH=/app

# Expose necessary ports
EXPOSE 8000  
#EXPOSE 6800  
EXPOSE 11434

# Default command for running the container
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
