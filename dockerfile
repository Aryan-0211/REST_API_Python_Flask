# Use the official Python image as a base
FROM python:3.11-slim

# Expose the application port
EXPOSE 5001

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Command to run the Flask application
CMD ["flask", "run"]
