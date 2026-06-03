# Ni – AI Personal Operating System

> Your intelligent companion for managing your digital life, productivity, learning, fitness, communication, and smart devices.

Ni is not just a chatbot. It is a complete AI-powered personal operating system designed to feel like a real intelligent companion that understands you, remembers important information, learns from your behavior, and assists across devices.

---

## Features

| Module | Capabilities |
|--------|-------------|
| **AI Conversation Engine** | Natural chat, Hindi + English, pluggable AI (mock / OpenAI / extensible), context-aware, personalized |
| **Personal Life Management** | Smart calendar, task manager, to-do lists, goal tracking, habit tracking with streaks, daily planning |
| **Study & Career Assistant** | Study planner, session logging, progress dashboard, time tracking |
| **Memory System** | Remember goals, preferences, projects; full-text search; tagged notes and memories |
| **Fitness & Wellness Hub** | Workout tracking, weight logs, water intake with daily goals, sleep tracking, health dashboard |
| **Finance Dashboard** | Expense tracking, budget planning, category breakdown, monthly reports, savings goals |
| **Arduino & IoT Support** | Device registration, sensor readings, automations (time/sensor/event triggers) |
| **Life OS Dashboard** | Central view: tasks, goals, study progress, fitness, expenses, notes, events, device status |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Framer Motion, Recharts |
| Backend | FastAPI (Python 3.12), SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL 16 |
| Auth | JWT (python-jose) + bcrypt |
| AI | Pluggable – Mock (built-in) or OpenAI GPT-4o-mini |
| Deployment | Docker Compose |

---

## Quick Start

```bash
# Clone
git clone https://github.com/nitttin-yadav/nitttin.git
cd nitttin

# Start with Docker
docker compose up --build

# Open
# Frontend:  http://localhost:3000
# API Docs:  http://localhost:8000/docs
```

See [Installation Guide](docs/INSTALLATION.md) for manual setup.

---

## Design

- **Dark mode** – deep space-inspired dark theme
- **Glassmorphism** – frosted glass cards with subtle glow effects
- **Smooth animations** – Framer Motion page and component transitions
- **Mobile-first** – responsive design with collapsible sidebar
- **Professional & premium** – clean typography, consistent design tokens

---

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [API Reference](docs/API.md)
- [Future Roadmap](docs/ROADMAP.md)

---

## Project Structure

```
nitttin/
├── backend/
│   ├── app/
│   │   ├── auth/          # Authentication (JWT, users)
│   │   ├── conversations/ # AI chat engine
│   │   ├── tasks/         # Tasks, goals, habits, calendar
│   │   ├── memory/        # Memories & notes
│   │   ├── fitness/       # Workouts, weight, water, sleep
│   │   ├── finance/       # Expenses, budgets, savings
│   │   ├── study/         # Study plans & sessions
│   │   ├── devices/       # IoT devices & automations
│   │   ├── dashboard/     # Aggregated Life OS dashboard
│   │   ├── main.py        # FastAPI app
│   │   ├── config.py      # Settings
│   │   └── database.py    # DB connection
│   ├── alembic/           # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── auth/          # Auth context, login, register
│   │   ├── components/    # Layout, Sidebar, GlassCard, StatCard
│   │   └── pages/         # Dashboard, Chat, Tasks, Memory, Fitness, Finance, Study, Devices, Settings
│   ├── package.json
│   └── Dockerfile
├── docs/                  # Documentation
├── docker-compose.yml     # Full-stack orchestration
└── README.md
```

---

## License

MIT
