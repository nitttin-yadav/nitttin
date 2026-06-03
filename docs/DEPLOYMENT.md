# Ni – Deployment Guide

## Docker Production Deployment

### 1. Build production images

```bash
docker compose -f docker-compose.yml build
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://ni_user:<strong-password>@db:5432/ni_db
SECRET_KEY=<generate-with: openssl rand -hex 32>
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

### 3. Deploy

```bash
docker compose up -d
```

---

## Cloud Deployment Options

### AWS / GCP / Azure

1. **Database**: Use a managed PostgreSQL service (RDS, Cloud SQL, Azure Database)
2. **Backend**: Deploy as a container on ECS, Cloud Run, or Azure Container Apps
3. **Frontend**: Build and deploy to S3 + CloudFront, or a CDN

### Railway / Render / Fly.io

1. Connect your GitHub repo
2. Set environment variables in the dashboard
3. Deploy backend and frontend as separate services
4. Add a PostgreSQL addon

### Vercel (Frontend) + Fly.io (Backend)

1. Frontend: `cd frontend && vercel`
2. Backend: `cd backend && fly launch`
3. Set `VITE_API_URL` in Vercel to point to your Fly.io backend

---

## SSL / HTTPS

For production, always use HTTPS. Options:
- **Let's Encrypt** with Caddy or Certbot
- **Cloudflare** proxy (free SSL)
- **Cloud provider** managed certificates

---

## Database Migrations

```bash
# Generate a new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Monitoring

- **Health check**: `GET /api/health`
- **API docs**: `/docs` (Swagger) or `/redoc` (ReDoc)
- Add Prometheus/Grafana or Datadog for production monitoring
