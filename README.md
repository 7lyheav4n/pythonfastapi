## Introduction

A production-style REST API with:
- FastAPI REST API
- PostgreSQL
- Docker + Docker Compose
- Clean project structure
- CRUD API


# Project Structure
```bash
fastapi-postgres/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── config.py
│   └── routers/
│       └── tasks.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md

```