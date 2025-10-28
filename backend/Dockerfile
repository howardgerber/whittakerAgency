# Multi-stage Dockerfile for FastAPI backend

# Development stage
FROM python:3.11-slim as development

WORKDIR /app

# Install system dependencies including MySQL client for wait script
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait script and make executable
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Copy application code
COPY . .

# Development command is specified in docker-compose.dev.yml
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5102", "--reload"]


# Production stage
FROM python:3.11-slim as production

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p /app/uploads

# Run as non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Production command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
