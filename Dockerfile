# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install git and any other necessary dependencies
RUN apt-get update && apt-get install -y git

# Define build arguments
ARG GITHUB_REPOSITORY
ARG TAG
ARG APP_MODULE
ARG APP_PORT

# Construct the repository URL
ARG REPO_PATH=https://github.com/${GITHUB_REPOSITORY}.git

# Install necessary Python dependencies
RUN pip install git+${REPO_PATH}@${TAG}
