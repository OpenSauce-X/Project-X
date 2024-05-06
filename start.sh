#!/bin/bash

# Pull the Docker image for the Flask application from Docker Hub
docker pull mrgeek001/website-monitoring-app

# Run MongoDB container
docker run -d --name my-mongodb mongo

# Wait for MongoDB to start
sleep 10

# Change directory to where docker-compose.yml is located
cd /Users/kartikprajapat/Downloads/content/project-X-test/Project-X

# Start the application with Docker Compose
docker-compose up -d