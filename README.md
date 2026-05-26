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

### 阿里云 / 国内 ECS 构建太慢

瓶颈通常在 **容器内 `apt-get` / `pip` / `npm`** 仍走国外源。`.env` 已支持（见 `.env.example`）：

```bash
APT_MIRROR=mirrors.aliyun.com
PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
NPM_REGISTRY=https://registry.npmmirror.com
PYTHON_IMAGE=...python:3.12-slim-bookworm   # 固定 bookworm，避免 trixie 源不稳定
```

在 ECS 上建议同时配置 Docker 守护进程镜像加速（`/etc/docker/daemon.json`）：

```json
{
  "registry-mirrors": [
    "https://registry.cn-hangzhou.aliyuncs.com",
    "https://docker.m.daocloud.io"
  ]
}
```

然后重新构建（无缓存首次会快很多）：

```bash
DOCKER_BUILDKIT=1 docker compose build --no-cache backend
docker compose up -d
```

第二次构建会命中层缓存，`apt-get` 一般不再重复执行。

### Alembic `alembic_version` / `pg_type_typname_nsp_index` 报错

多为 **backend 与 crawler 同时执行** `alembic upgrade` 导致。已在 compose 中改为仅 backend 迁移。

在 ECS 上修复一次：

```bash
docker compose exec postgres psql -U phdpilot -d phdpilot -c \
  "DROP TABLE IF EXISTS alembic_version CASCADE; DROP TYPE IF EXISTS alembic_version CASCADE;"

docker compose up -d --force-recreate backend crawler
```

若业务表已存在且仅需对齐版本：`docker compose exec backend alembic stamp head`

若 `phdpilot-backend is unhealthy`：先看日志 `docker compose logs backend --tail 80`。常见原因是迁移失败或 `--reload` 与健康检查冲突（已改为 `scripts/docker-entrypoint.sh` 且去掉 reload）。

若报 `type "userrole" already exists`（半迁移状态），在 ECS 上清空库后重启：

```bash
docker compose exec -T postgres psql -U phdpilot -d phdpilot < backend/scripts/reset_db.sql
docker compose up -d --force-recreate backend
```

**会删除所有业务数据**，仅适合首次部署或测试环境。

### 前端容器反复 `Killed`（OOM）

ECS 内存不足时，`npm ci && npm run dev` 会被系统杀掉。请用**生产 compose**（Next.js standalone，约 150–300MB）：

```bash
# .env 里设置公网访问地址，例如：
# NEXT_PUBLIC_API_URL=http://你的公网IP/api
# CORS_ORIGINS=http://你的公网IP

docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
```

内存 ≤2GB 时先不要启 crawler，稳定后再：`docker compose -f docker-compose.prod.yml --profile crawler up -d crawler`

可加 2G swap（可选）：

```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
```

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
