FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev docker.io && \
    pip install --upgrade pip

# Copy requirements and install them
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project into the container
COPY . /app/

# Expose necessary ports
EXPOSE 8000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
