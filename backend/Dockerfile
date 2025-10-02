# Official FastAPI Dockerfile pattern
# Based on: https://fastapi.tiangolo.com/deployment/docker/

FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements.txt

# Copy application code and tests
COPY ./app /code/app
COPY ./tests /code/tests

# Create directory for SQLite database
RUN mkdir -p /code/data

# Run lint checks during build (fail early on style issues)
RUN make -C /code lint-ci

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:80/health')" || exit 1

# Run the application with proxy headers enabled (for correct HTTPS redirects behind proxies)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--forwarded-allow-ips", "*"]
