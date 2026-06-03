# Ni – Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Ni – AI Personal OS                   │
├──────────────────────┬──────────────────────────────────┤
│    React Frontend    │         FastAPI Backend           │
│   (Vite + TS + TW)  │   (Python 3.12 + SQLAlchemy)     │
├──────────────────────┼──────────────────────────────────┤
│                      │                                   │
│  ┌─ Auth ──────────┐ │  ┌─ Auth ────────────────────┐   │
│  │ Login/Register  │ │  │ JWT · bcrypt · OAuth2     │   │
│  └─────────────────┘ │  └───────────────────────────┘   │
│                      │                                   │
│  ┌─ Dashboard ─────┐ │  ┌─ Modules ─────────────────┐   │
│  │ Life OS View    │ │  │ conversations (AI engine)  │   │
│  │ Stats + Events  │ │  │ tasks / goals / habits     │   │
│  └─────────────────┘ │  │ memory / notes             │   │
│                      │  │ fitness (workout/water/     │   │
│  ┌─ Feature Pages ─┐ │  │   sleep/weight)            │   │
│  │ Chat            │ │  │ finance (expenses/budget/  │   │
│  │ Tasks & Goals   │ │  │   savings)                 │   │
│  │ Memory          │ │  │ study (plans/sessions)     │   │
│  │ Fitness         │ │  │ devices (IoT/automations)  │   │
│  │ Finance         │ │  │ dashboard (aggregated)     │   │
│  │ Study           │ │  └───────────────────────────┘   │
│  │ Devices         │ │                                   │
│  │ Settings        │ │  ┌─ AI Layer ────────────────┐   │
│  └─────────────────┘ │  │ Pluggable providers:      │   │
│                      │  │  · mock (built-in)         │   │
│                      │  │  · openai (GPT-4o-mini)    │   │
│                      │  └───────────────────────────┘   │
├──────────────────────┴──────────────────────────────────┤
│                   PostgreSQL 16                          │
│   20+ tables · UUID PKs · timezone-aware timestamps     │
└─────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### Modular Architecture
Each feature domain is a self-contained module with its own:
- `models.py` – SQLAlchemy ORM models
- `schemas.py` – Pydantic request/response schemas
- `router.py` – FastAPI endpoints

This makes the system easy to extend — adding a new module is as simple as creating a new folder with these three files and registering the router in `main.py`.

### Pluggable AI Engine
The conversation system uses a provider pattern (`ai_engine.py`):
- `MockProvider` – works out of the box with no API keys
- `OpenAIProvider` – connects to GPT-4o-mini (or any OpenAI model)
- Easy to extend with Anthropic, local LLMs, etc.

### Database Design
- All primary keys are UUIDs for distributed-readiness
- All timestamps are timezone-aware
- Relationships use cascading deletes for data integrity
- PostgreSQL ARRAY type for tags (memory, notes)

### Frontend Architecture
- React 18 + TypeScript for type safety
- Tailwind CSS with custom Ni design tokens
- Glassmorphism design system (frosted glass cards, glow effects)
- Framer Motion for smooth page and component animations
- Mobile-first responsive design with collapsible sidebar
- Centralized API client with JWT token management

### Security
- JWT-based authentication with bcrypt password hashing
- All API endpoints are protected (except auth endpoints)
- CORS configured for development and production
- No secrets stored in code (environment variables)
