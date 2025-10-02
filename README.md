# Movie Explorer Platform

Full‑stack Movie Explorer with FastAPI (Python) + React (Vite + TypeScript). Browse movies, actors, directors, and genres with backend‑driven filtering and clean UI.

## Live
- Backend (Swagger UI): https://l7informaticaassessment-production.up.railway.app/docs
- Frontend: https://l7informaticaassessment-production-9114.up.railway.app/
- Backend Image: https://github.com/pnavin9/L7_informatica_assessment/pkgs/container/l7-informatica-assessment
- Frontend Image: https://github.com/pnavin9/L7_informatica_assessment/pkgs/container/l7-informatica-frontend

## What’s implemented (spec coverage)
- Core entities: Movies, Actors, Directors, Genres (+ Ratings)
- Relations: many‑to‑many Movies↔Genres, many‑to‑many Movies↔Actors, one Movie→Director
- Backend filters (no frontend filtering):
  - Movies: `genre`, `director`, `actor`, `year`, `min_year`, `max_year`, `status`, `search`
  - Actors: `genre`, `movie`, `search`
  - Directors: `genre`, `search`
  - Genres: `search`
- Unified movie search: `GET /api/movies/search?q=<term>` (OR across title, director, actor, genre)
- Frontend (Vite + React + TS), Tailwind CSS styling
- API documented via Swagger/OpenAPI
- Dockerized frontend + backend with `docker-compose`
- Linting and unit tests in frontend and backend
- Edge case handling documented (see EDGE_CASES.md)
- No auth (by requirement)

## Quickstart (Docker Compose)
Prereq: Docker + Docker Compose

```bash
git clone <repo-url>
cd L7_informatica_assessment
docker-compose up -d --build

# Frontend
open http://localhost:5173/
# Backend docs
open http://localhost:8000/docs
```

## Run locally (without containers)
Backend:
```bash
cd backend
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Frontend:
```bash
cd frontend
nvm use 20
npm install
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

## Environment
- `VITE_API_BASE_URL`: Base URL used by the frontend to call the API (see `frontend/src/services/api.ts`).

## API overview (selected)
- Movies
  - `GET /api/movies` query: `genre`, `director`, `actor`, `year`, `min_year`, `max_year`, `status`, `search`, `skip` (>=0), `limit` (1..100)
  - `GET /api/movies/search?q=` unified OR search
  - `GET /api/movies/{id}` details
- Actors
  - `GET /api/actors` query: `genre`, `movie`, `search`, `skip`, `limit`
  - `GET /api/actors/{id}` details
- Directors
  - `GET /api/directors` query: `genre`, `search`, `skip`, `limit`
  - `GET /api/directors/{id}` details
- Genres
  - `GET /api/genres` query: `search`
  - `GET /api/genres/{id}`
- Ratings
  - `GET /api/movies/{movie_id}/ratings`
  - `POST /api/ratings` (body: `movie_id`, `score`, optional `review`)

Examples:
```bash
curl "http://localhost:8000/api/movies?genre=Action&min_year=2000&max_year=2010"
curl "http://localhost:8000/api/movies/search?q=Nolan"
curl "http://localhost:8000/api/actors?genre=Drama"
```

## Frontend features
- Browse movies, filter by genre/actor/director/year range
- Search (when no filters applied) with results count
- Movie detail page with cast, director, genres, ratings
- Actor/Director profile pages with filmography
- Loading and basic error states

## Testing & lint
Backend:
```bash
cd backend
pytest -q
```
Frontend:
```bash
cd frontend
npm run lint
npm run test:run
npm run build
```

## Docker images
Backend:
```bash
docker pull ghcr.io/pnavin9/l7-informatica-assessment:prod-latest
docker run -p 8000:80 ghcr.io/pnavin9/l7-informatica-assessment:prod-latest
```
Frontend:
```bash
docker pull ghcr.io/pnavin9/l7-informatica-frontend:sha-<tag>
docker run -p 5173:80 -e VITE_API_BASE_URL="http://localhost:8000" ghcr.io/pnavin9/l7-informatica-frontend:sha-<tag>
```

## Health & ops
```bash
curl http://localhost:8000/health
docker-compose logs backend
docker-compose down
```

## Edge cases
See `EDGE_CASES.md` for documented scenarios and behavior.

## License
MIT
