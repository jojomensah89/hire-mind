# Backend Structure (FastAPI)

This document outlines the structure of the FastAPI backend for the AI Job Board.

## Core Principles

*   **Modularity:** The backend is organized into modules, with each module responsible for a specific domain (e.g., `jobs`, `users`).
*   **Dependency Injection:** FastAPI's dependency injection system is used to manage dependencies and promote loose coupling.
*   **Clear Separation of Concerns:** The code is structured to separate business logic, data access, and API endpoints.

## Directory Structure

```
backend/
├── alembic/              # Database migration scripts
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── jobs.py
│   │       │   └── users.py
│   │       └── deps.py       # API dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py     # Configuration settings
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── crud_job.py
│   │   └── crud_user.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py         # Base model and session
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── job.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── job.py
│   │   └── user.py
│   └── main.py             # Main FastAPI application
├── requirements.txt
└── uvicorn.py
```

## Key Components

*   **`main.py`**: The entry point for the FastAPI application.
*   **`app/api/v1/endpoints/`**: Contains the API endpoint definitions for different resources (e.g., `jobs.py`, `users.py`).
*   **`app/crud/`**: Houses the Create, Read, Update, Delete (CRUD) operations for interacting with the database.
*   **`app/models/`**: Defines the SQLAlchemy database models.
*   **`app/schemas/`**: Defines the Pydantic schemas for data validation and serialization.
*   **`app/db/`**: Manages the database connection and session.
*   **`app/core/config.py`**: Handles application configuration and environment variables.
