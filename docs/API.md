# Ni – API Reference

Base URL: `http://localhost:8000/api`

All endpoints (except auth) require `Authorization: Bearer <token>` header.

---

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Login, returns JWT |
| GET | `/auth/me` | Get current user |
| PATCH | `/auth/me` | Update profile |

## Conversations (AI Chat)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/conversations/` | List conversations |
| POST | `/conversations/` | Create conversation |
| GET | `/conversations/{id}` | Get conversation + messages |
| POST | `/conversations/{id}/messages` | Send message, get AI reply |
| DELETE | `/conversations/{id}` | Delete conversation |

## Tasks & Life Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | List tasks (filter by status) |
| POST | `/tasks/` | Create task |
| PATCH | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/goals` | List goals |
| POST | `/tasks/goals` | Create goal |
| PATCH | `/tasks/goals/{id}` | Update goal |
| GET | `/tasks/habits` | List habits |
| POST | `/tasks/habits` | Create habit |
| POST | `/tasks/habits/{id}/log` | Log habit completion |
| GET | `/tasks/events` | List upcoming events |
| POST | `/tasks/events` | Create calendar event |

## Memory System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/memory/` | List/search memories |
| POST | `/memory/` | Create memory |
| PATCH | `/memory/{id}` | Update memory |
| DELETE | `/memory/{id}` | Delete memory |
| GET | `/memory/notes` | List notes |
| POST | `/memory/notes` | Create note |
| PATCH | `/memory/notes/{id}` | Update note |

## Fitness & Wellness

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/fitness/dashboard` | Fitness overview |
| GET | `/fitness/workouts` | List workouts |
| POST | `/fitness/workouts` | Log workout |
| GET | `/fitness/weight` | Weight history |
| POST | `/fitness/weight` | Log weight |
| GET | `/fitness/water` | Today's water logs |
| POST | `/fitness/water` | Log water intake |
| GET | `/fitness/water/today` | Water intake summary |
| GET | `/fitness/sleep` | Sleep history |
| POST | `/fitness/sleep` | Log sleep |

## Finance Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/finance/expenses` | List expenses (by month) |
| POST | `/finance/expenses` | Create expense |
| DELETE | `/finance/expenses/{id}` | Delete expense |
| GET | `/finance/budgets` | List budgets |
| POST | `/finance/budgets` | Create budget |
| GET | `/finance/savings` | List savings goals |
| POST | `/finance/savings` | Create savings goal |
| PATCH | `/finance/savings/{id}` | Update savings goal |
| GET | `/finance/report` | Monthly report |

## Study & Career

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/study/dashboard` | Study overview |
| GET | `/study/plans` | List study plans |
| POST | `/study/plans` | Create study plan |
| GET | `/study/plans/{id}` | Get plan details |
| GET | `/study/sessions` | List study sessions |
| POST | `/study/sessions` | Log study session |

## Devices & IoT

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/devices/` | List devices |
| POST | `/devices/` | Register device |
| POST | `/devices/{id}/readings` | Post sensor reading |
| GET | `/devices/{id}/readings` | Get device readings |
| DELETE | `/devices/{id}` | Remove device |
| GET | `/devices/automations` | List automations |
| POST | `/devices/automations` | Create automation |
| PATCH | `/devices/automations/{id}/toggle` | Toggle automation |

## Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/` | Life OS dashboard (all metrics) |

## Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
