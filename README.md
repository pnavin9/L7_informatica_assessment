# Movie Explorer API

FastAPI backend with SQLite database and comprehensive filtering.

## Setup & Run

### Prerequisites
- Docker & Docker Compose

### Start Application

```bash
# Clone and navigate
git clone <repo-url>
cd L7_informatica_assessment

# Start application
docker-compose up -d

# Access API documentation
open http://localhost:8000/docs
```

## API Usage

### Main Endpoints
- **Health Check**: `GET /health`
- **Movies**: `GET /api/movies/`
- **API Documentation**: `GET /docs`

### Example Requests

```bash
# Get all movies
curl "http://localhost:8000/api/movies/"

# Filter by genre
curl "http://localhost:8000/api/movies/?genre=Action"

# Search movies
curl "http://localhost:8000/api/movies/?search=Inception"
```

## Health Checks

### Check if API is running

```bash
# Basic health check
curl http://localhost:8000/health

# Expected response: {"status":"healthy"}
```

### Check container status

```bash
# View container logs
docker-compose logs backend

# Stop application
docker-compose down
```

## Tech Stack

- **Backend**: FastAPI + SQLite
- **Container**: Docker + Docker Compose
- **Documentation**: Auto-generated Swagger UI