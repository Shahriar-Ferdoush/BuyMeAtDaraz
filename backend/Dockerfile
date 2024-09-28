# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Playwright and minimal build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  poppler-utils \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install & setup Poetry, and configure it to create a virtualenv inside the container
RUN pip install --no-cache-dir poetry

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/
# This command will avoid creating cache for installed packages
RUN poetry install --no-interaction --no-ansi --no-cache

# Install Playwright Chromium with required dependencies
RUN pip install --no-cache-dir playwright && playwright install --with-deps chromium

# Copy the rest of the application code to the container
COPY ./buymeatdaraz /app

# Expose the port your app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
