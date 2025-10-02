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

# Start application (backend + frontend)
docker-compose up -d --build

# Access Frontend (served by Nginx)
open http://localhost:5173/

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

## Frontend ↔ Backend connectivity

The frontend uses `VITE_API_BASE_URL` at build/runtime to reach the backend. In Compose, services share a network and can reach each other via DNS names (service name).

- In `docker-compose.yml`, the frontend is built with:
  - `VITE_API_BASE_URL=http://backend:80`
- The frontend code reads `import.meta.env.VITE_API_BASE_URL` and prefixes requests (see `frontend/src/services/api.ts`).
- When running locally without Compose, you can override with:

```bash
cd frontend
VITE_API_BASE_URL=http://localhost:8000 npm run dev
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
#Dummy Deploy2
