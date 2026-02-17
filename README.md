# ProGym Subscription Platform

Production-grade subscription SaaS with FastAPI, React, PostgreSQL, Razorpay integration, JWT authentication, and role-based admin dashboard.

## Architecture
- **Frontend**: React + Tailwind CSS + React Router
- **Backend**: FastAPI + SQLAlchemy + JWT + Argon2 password hashing
- **Database**: PostgreSQL
- **Payments**: Razorpay order creation + signature verification
- **Infra**: Docker Compose + Nginx reverse proxy

## Folder structure
```
backend/
  app/
    api/routes/        # Auth, user, subscription, payment, admin REST endpoints
    core/              # Settings and security primitives
    db/                # SQLAlchemy engine and declarative base
    models/            # User, Subscription, Payment, Token blocklist models
    schemas/           # Pydantic request/response contracts
    services/          # Domain services (plans)
  scripts/             # Admin seed script
frontend/
  src/
    api/               # Axios API client
    components/        # Reusable UI components
    contexts/          # Auth context + session state
    pages/             # Landing, pricing, auth, user/admin dashboards
nginx/                 # Reverse proxy config
```

## Core security controls
- Argon2 password hashing
- JWT access + refresh tokens
- Token blocklist for logout session invalidation
- Role-based authorization guards for admin endpoints
- Pydantic validation on all request models
- SQLAlchemy ORM to prevent SQL injection
- CORS restrictions and proxy-ready for HTTPS termination

## Run with Docker
```bash
docker compose up --build
```

## Default seeded admin
Run after backend is started:
```bash
docker compose exec backend python scripts/seed_admin.py
```

Credentials: `admin@progym.com / Admin@12345`

## API examples
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/subscriptions`
- `POST /api/subscriptions/create`
- `POST /api/payments/create-order`
- `POST /api/payments/verify`
- `GET /api/admin/users`
- `GET /api/admin/payments`
- `GET /api/admin/subscriptions`
- `GET /api/admin/analytics`
