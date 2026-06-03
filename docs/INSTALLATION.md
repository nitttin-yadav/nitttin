# Ni – Installation Guide

## Prerequisites

- **Docker + Docker Compose** (recommended) — OR:
- Python 3.12+, Node.js 20+, PostgreSQL 16+

---

## Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/nitttin-yadav/nitttin.git
cd nitttin

# Start all services
docker compose up --build

# Access:
#   Frontend: http://localhost:3000
#   Backend API: http://localhost:8000
#   API Docs: http://localhost:8000/docs
```

---

## Option 2: Manual Setup

### 1. Database

```bash
# Start PostgreSQL (if not running)
# Create the database
createdb ni_db
psql -c "CREATE USER ni_user WITH PASSWORD 'ni_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE ni_db TO ni_user;"
```

### 2. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# → http://localhost:5173
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://ni_user:ni_password@localhost:5432/ni_db` | PostgreSQL connection string |
| `SECRET_KEY` | `change-me-in-production` | JWT signing key |
| `AI_PROVIDER` | `mock` | `mock` or `openai` |
| `OPENAI_API_KEY` | (empty) | Required if AI_PROVIDER=openai |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use |

---

## First Steps

1. Open the app (http://localhost:3000 or http://localhost:5173)
2. Click "Create Account" to register
3. Explore the Dashboard, Chat with Ni, add Tasks, track Fitness, etc.
