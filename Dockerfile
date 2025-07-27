# Use official Python 3.8 base image
FROM python:3.8-slim

# Expose port 8080 for GCP or Docker
EXPOSE 8080

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "app.py"]
