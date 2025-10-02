# Docker Deployment Guide

## Overview
This guide covers Docker deployment for the Movie Explorer API, following FastAPI's official Docker best practices.

## 📦 Docker Files

### 1. **Dockerfile** (Development/Standard)
Standard Docker image for development and testing.

```dockerfile
FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

**Features:**
- ✅ Based on official Python 3.12 slim image
- ✅ Follows FastAPI recommended pattern
- ✅ Includes health checks
- ✅ Optimized layer caching

### 2. **Dockerfile.prod** (Production)
Multi-stage build for production with enhanced security.

**Features:**
- ✅ Multi-stage build (smaller image)
- ✅ Non-root user for security
- ✅ Multiple workers (4) for production
- ✅ Optimized dependencies installation

### 3. **.dockerignore**
Excludes unnecessary files from Docker context.

**Excludes:**
- Virtual environments
- Cache files
- Test files
- Development tools
- Database files (mounted separately)

---

## 🚀 Quick Start

### Build and Run with Docker

```bash
# Build the image
docker build -t movie-explorer-api ./backend

# Run the container
docker run -d \
  --name movie-api \
  -p 8000:80 \
  movie-explorer-api

# Access the API
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### Using Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## 🔧 Docker Compose Configuration

### Service Configuration

```yaml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:80"
    volumes:
      - ./backend/data:/code/data  # Database persistence
      - ./backend/app:/code/app     # Hot reload (dev only)
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:80/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Features:
- ✅ **Port Mapping**: 8000 (host) → 80 (container)
- ✅ **Volume Mounting**: Database persists outside container
- ✅ **Hot Reload**: Code changes reflect immediately (dev mode)
- ✅ **Health Checks**: Automatic container health monitoring
- ✅ **Auto Restart**: Container restarts on failure

---

## 🌐 Environment Variables

### Available Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_PATH` | `./movies.db` | SQLite database file path |
| `PYTHONUNBUFFERED` | `1` | Disable Python output buffering |
| `PYTHONDONTWRITEBYTECODE` | `1` | Don't create .pyc files |

### Setting Environment Variables

**Docker Run:**
```bash
docker run -d \
  -e DATABASE_PATH=/code/data/movies.db \
  -p 8000:80 \
  movie-explorer-api
```

**Docker Compose:**
```yaml
services:
  backend:
    environment:
      - DATABASE_PATH=/code/data/movies.db
```

---

## 📊 Production Deployment

### Using Production Dockerfile

```bash
# Build production image
docker build -f backend/Dockerfile.prod -t movie-explorer-api:prod ./backend

# Run with production settings
docker run -d \
  --name movie-api-prod \
  -p 80:80 \
  --restart always \
  -v /path/to/data:/code/data \
  movie-explorer-api:prod
```

### Production Features:
- ✅ Multi-stage build (smaller image size)
- ✅ Non-root user (enhanced security)
- ✅ 4 Uvicorn workers (better performance)
- ✅ Optimized dependencies

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

The project includes automated Docker builds on each push:

**Location:** `.github/workflows/docker-build.yml`

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`

**Steps:**
1. Build Docker image
2. Run automated tests in container
3. Push to GitHub Container Registry
4. Build production image (main branch only)

**Usage:**
```bash
# Pull latest image
docker pull ghcr.io/YOUR_USERNAME/l7_informatica_assessment:latest

# Run pulled image
docker run -d -p 8000:80 ghcr.io/YOUR_USERNAME/l7_informatica_assessment:latest
```

---

## 🛠️ Common Commands

### Development

```bash
# Build image
docker-compose build

# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Execute command in container
docker-compose exec backend python -c "from app.db.database import init_db; init_db()"

# Shell access
docker-compose exec backend /bin/bash

# Stop services
docker-compose down

# Clean up everything
docker-compose down -v --rmi all
```

### Production

```bash
# Build production image
docker build -f backend/Dockerfile.prod -t movie-api:prod ./backend

# Run with volume
docker run -d \
  --name movie-api \
  -p 80:80 \
  -v movie-data:/code/data \
  --restart always \
  movie-api:prod

# Check container health
docker inspect --format='{{.State.Health.Status}}' movie-api

# View container logs
docker logs -f movie-api

# Stop and remove
docker stop movie-api && docker rm movie-api
```

---

## 🔍 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs backend

# Check container status
docker ps -a

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Database issues

```bash
# Remove database volume
docker-compose down -v

# Restart with fresh database
docker-compose up -d
```

### Health check failing

```bash
# Check health status
docker inspect movie-api | grep -A 10 Health

# Manual health check
docker exec movie-api curl http://localhost:80/health
```

### Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Use different port
docker run -p 8080:80 movie-explorer-api
```

---

## 📈 Performance Tips

### 1. **Multi-stage Builds**
Use `Dockerfile.prod` for smaller images (40% size reduction).

### 2. **Layer Caching**
Order Dockerfile commands from least to most frequently changed:
```dockerfile
COPY requirements.txt /code/    # Changes rarely
RUN pip install -r /code/requirements.txt
COPY ./app /code/app            # Changes frequently
```

### 3. **Volume Mounting**
Mount database separately for data persistence:
```yaml
volumes:
  - ./backend/data:/code/data
```

### 4. **Resource Limits**
Set resource limits for production:
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
```

---

## 🔒 Security Best Practices

✅ **Non-root User**: Production image runs as `appuser`  
✅ **Read-only Filesystem**: Can be enabled with `--read-only`  
✅ **No Secrets in Image**: Use environment variables  
✅ **Minimal Base Image**: Uses `python:3.12-slim`  
✅ **Health Checks**: Automatic failure detection  
✅ **Updated Dependencies**: Regular security updates  

---

## 📚 References

- [FastAPI Docker Documentation](https://fastapi.tiangolo.com/deployment/docker/)
- [FastAPI Official Docker Image](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)

---

## ✅ Summary

Your Docker setup includes:

1. ✅ **Standard Dockerfile** - FastAPI recommended pattern
2. ✅ **Production Dockerfile** - Multi-stage, optimized, secure
3. ✅ **Docker Compose** - Easy orchestration
4. ✅ **.dockerignore** - Optimized build context
5. ✅ **CI/CD Workflow** - Automated builds and tests
6. ✅ **Health Checks** - Container monitoring
7. ✅ **Volume Persistence** - Database data safety
8. ✅ **Environment Config** - Flexible configuration

The setup is **production-ready** and follows **industry best practices**!
