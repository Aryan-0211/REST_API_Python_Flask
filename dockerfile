# Use the official Python image as a base
FROM python:3.11-slim

# Expose the application port
#EXPOSE 5001

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY . .

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
