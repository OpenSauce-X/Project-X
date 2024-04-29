# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY website_monitoring /app/website_monitoring

# Copy the requirements.txt file into the container
COPY requirements.txt /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=website_monitoring/app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
