#Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py

# Set the working directory
WORKDIR /app

# Install postgres client
RUN apt-get update && apt-get install -y postgresql-client

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY . .

# Make the entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Command to run the Flask application with Gunicorn
CMD ["/bin/bash", "docker-entrypoint.sh"]
