# Edge Cases and Error Handling

This document outlines notable scenarios and how the system behaves (backend + frontend).

## Empty datasets
- On a fresh run, the backend seeds sample data automatically. If the DB is cleared, list endpoints return `[]`.
- Frontend displays the count (e.g., "0 movies found") and renders an empty grid without crashing.

## Invalid IDs
- `GET /api/movies/{id}`, `GET /api/actors/{id}`, `GET /api/directors/{id}`, `GET /api/genres/{id}`
  - Returns `404` with `{ "detail": "<Entity> not found" }` if the entity is missing.
- Ratings endpoints follow similar `404` for missing movie/rating IDs.

## Invalid filters / types
- Movie filters (`year`, `min_year`, `max_year`) must be integers; invalid types are rejected by FastAPI validation with `422`.
- Unknown `genre`, `actor`, `director`, or `status` values yield a valid `200` with an empty list if no matches.
- `skip` must be `>= 0`, `limit` must be within `1..100` (enforced by FastAPI).

## Pagination & limits
- Movies endpoint supports `skip` and `limit` with sane bounds to protect the DB.
- Frontend currently fetches without explicit pagination UI; URL parameters can be extended without code changes.

## Search vs filters precedence
- When any movie filter is present, the frontend calls `GET /api/movies` with filters.
- When no filters are present and `q` exists, frontend uses `GET /api/movies/search?q=...`.

## Network/API failures
- Frontend shows a friendly error state on fetch failure (e.g., backend down or non‑2xx response).
- The API client has a 15s timeout and basic in‑memory GET caching; errors bubble up as messages.

## Data integrity gaps
- Creating a movie validates `director_id` exists; otherwise `404 Director not found`.
- Creating a rating validates `movie_id` exists; otherwise `404 Movie not found`.
- Updating movies replaces provided `genre_ids`/`actor_ids` sets when present.

## Case‑insensitive matching
- Filters use `ILIKE` (`%value%`) for `genre`, `director`, `actor`, `status`, and `search` to allow case‑insensitive partial matches.

## Performance considerations
- Backend uses eager loading (`joinedload`) on details and lists to avoid N+1 queries.
- Frontend caches GET responses for ~30s by default to reduce duplicate calls.

## Rate limits & timeouts
- No server rate limiting is enforced. Client timeout is 15s with abort support.
- If needed, add server throttling or CDN caching in front of `/api/`.

## Security
- CORS allows all origins for demo purposes. In production, restrict `allow_origins` to known hosts.

## Accessibility & UX
- Loading skeletons are shown during async fetch.
- Inputs validate numeric ranges for year fields.

## Known not‑implemented (explicit)
- No authentication/authorization (as specified).
- No persistent favorites/watch‑later; can be added via localStorage.


