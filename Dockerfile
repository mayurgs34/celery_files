#
#!/usr/bin/python3.8 
#
# File: Dockerfile
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: docker file for creating flask docker image
# for the stryker's audio data capturing tool application. 
#


# Use a base image with Python and install dependencies
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .
# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the Flask application port
EXPOSE 8080

# Run the Flask application

CMD ["gunicorn", "--workers=2", "--threads=2", "--bind", "0.0.0.0:8080", "app:app"]
