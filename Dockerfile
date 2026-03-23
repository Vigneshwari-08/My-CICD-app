# Use official slim Python image — smaller = faster deploys
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies FIRST (Docker layer caching)
# If requirements.txt hasn't changed, this layer is reused
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app/ ./app/

# Set environment variable
ENV APP_VERSION=1.0.0

# Expose the port the app listens on
EXPOSE 5000

# Use Gunicorn (production WSGI server) not Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.main:app"]
