# PhD Pilot

AI Copilot for European PhD Applications — MVP Phase 1.

## Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL + pgvector, Redis
- **Deploy**: Docker Compose + Nginx

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

### Docker Hub 拉取超时（国内网络）

若出现 `failed to fetch anonymous token ... i/o timeout`，`.env` 已默认配置 **DaoCloud 镜像**（`docker.m.daocloud.io/...`）。确认 `.env` 包含：

```bash
POSTGRES_IMAGE=docker.m.daocloud.io/pgvector/pgvector:pg16
REDIS_IMAGE=docker.m.daocloud.io/library/redis:7-alpine
NGINX_IMAGE=docker.m.daocloud.io/library/nginx:alpine
PYTHON_IMAGE=docker.m.daocloud.io/library/python:3.12-slim
NODE_IMAGE=docker.m.daocloud.io/library/node:20-alpine
```

也可在 **Docker Desktop → Settings → Docker Engine** 配置全局加速：

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live"
  ]
}
```

保存后 **Restart Docker**，再执行 `docker compose up --build`。

| URL | Service |
|-----|---------|
| http://localhost | Frontend (via Nginx) |
| http://localhost/api/docs | API documentation |
| http://localhost:8000 | Backend (direct) |
| http://localhost:3000 | Frontend (direct) |

### Seed sample positions (dev)

```bash
docker compose exec backend python scripts/seed.py
```

### Run position crawler (EURAXESS)

```bash
# One-off run
docker compose exec crawler python -m app.crawler.tasks.daily_update --once

# Or start crawler service (runs on startup + daily 03:00 UTC)
docker compose up -d crawler
```

Admin trigger (requires admin user):

```bash
curl -X POST http://localhost/api/admin/crawler/run \
  -H "Authorization: Bearer <admin_token>"
```

## Phase 1 (current)

- [x] Docker Compose (postgres, redis, backend, frontend, nginx)
- [x] User registration / login (JWT)
- [x] Credits system (signup bonus, feature costs API)
- [x] Database schema + Alembic migrations
- [x] Landing page + dashboard shell
- [x] Positions list API + UI
- [x] LLM provider abstraction stub

## Next phases

- **Phase 2**: Crawler, position search enhancements, application workspace
- **Phase 3**: AI match, supervisor analysis, outreach generation
- **Phase 4**: Payments, PRO membership, admin panel

## Project structure

```
eur_web/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── nginx/             # Reverse proxy
├── docker-compose.yml
└── 项目说明.md         # Full product spec
```

## Development (local, without Docker)

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+asyncpg://phdpilot:phdpilot_secret@localhost:5432/phdpilot
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
export NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```
# phdpilot
