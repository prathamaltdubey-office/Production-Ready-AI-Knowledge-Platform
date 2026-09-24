# Deployment Guide — Production-Ready AI Knowledge Platform

This guide covers running the full application (backend + frontend + local LLM) using containers, on a single machine.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Podman (or Docker) | This project uses `Containerfile` (Podman-style naming), compatible with both Podman and Docker |
| Podman Compose (or Docker Compose) | `podman compose` / `docker compose` |
| Ollama | Installed and running on the host machine (not containerized) |
| Git | To clone the repository |

> **Windows users:** Podman requires a Linux VM to run containers (via WSL2). See the [Troubleshooting Guide](./troubleshooting-guide.md) if `podman machine start` fails.

---

## 1. Clone the repository

```bash
git clone <repository-url>
cd week-4
```

## 2. Install and start Ollama (host machine)

Ollama runs directly on the host, not inside a container, so the backend container can reach it via `host.containers.internal`.

```bash
ollama serve
ollama pull llama3   # or gemma, mistral, phi — whichever model the project uses
```

Confirm Ollama is reachable:

```bash
curl http://localhost:11434
```

## 3. Configure environment variables

This project uses **two** `.env` files — one at the project root (used by the backend and by Compose to resolve build args) and one inside `frontend/` (used by the frontend container).

### Root `.env`

Create `.env` in the project root:

```env
API_TOKEN=your-secret-token-here
OLLAMA_BASE_URL=http://host.containers.internal:11434
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TOKEN=your-secret-token-here
```

### `frontend/.env`

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TOKEN=your-secret-token-here
```

> **Important:** `API_TOKEN` and `VITE_API_TOKEN` must match — the frontend sends this token to authenticate against the backend's `HTTPBearer` check. Never commit real `.env` files; use `.env.example` files (with placeholder values) for reference instead.

## 4. Build and start the containers

```bash
podman compose up --build
```

*(or `docker compose up --build` if using Docker instead of Podman)*

This builds and starts two services:

| Service | Container name | Port | Built from |
| --- | --- | --- | --- |
| Backend (FastAPI) | `churn-backend` | `8000` | `Containerfile` (root) |
| Frontend (React/Vite) | `churn-frontend` | `5173` | `frontend/Containerfile` |

## 5. Verify the deployment

**Backend health check:**

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{ "status": "healthy", "ollama": "up", "faiss_index": "loaded" }
```

If `ollama` shows `"down"`, confirm `ollama serve` is running on the host and that `OLLAMA_BASE_URL` in `.env` is correct.

**Frontend:** Open `http://localhost:5173` in a browser. The chat interface and prediction form should load and successfully call the backend.

**Interactive API docs:** FastAPI's auto-generated docs are available at `http://localhost:8000/docs`.

## 6. Stopping the deployment

```bash
podman compose down
```

## 7. Rebuilding after code changes

```bash
podman compose down
podman compose up --build
```

## 8. Volumes and persisted data

| Host path | Container path | Purpose |
| --- | --- | --- |
| `./documents` | `/app/documents` | Uploaded documents used by the RAG pipeline persist across restarts |
| `./backend/logs` | `/app/backend/logs` | Structured application/error logs persist across restarts |

## 9. CI/CD

Every push to `main`/`master` (and every pull request) triggers `.github/workflows/ci.yml`, which runs four jobs: backend tests, frontend build, lint checks (Ruff/Black/isort), and Docker build validation for both containers. A green CI run is a strong signal that the current commit will deploy cleanly using the steps above.

## 10. Production considerations (beyond this local setup)

These are not implemented in the current project but worth noting for anyone extending it toward a real production deployment:

- Replace the static `API_TOKEN` with a proper auth provider (OAuth2/JWT with expiry and refresh)
- Move secrets to a secret manager rather than `.env` files
- Add TLS termination (reverse proxy such as Nginx/Caddy) in front of both services
- Add resource limits and health-check directives to `compose.yaml` for production-grade container orchestration