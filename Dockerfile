# Use the official Python image as the base image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install system packages, including SQLite3
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define the command to run when the container starts
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]
