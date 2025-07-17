# Project Structure

## Repository Organization

The project follows a monorepo structure with clear separation between frontend and backend:

```
/
├── frontend/           # Next.js frontend application
├── backend/            # FastAPI backend application
├── docs/               # Project documentation
├── system/             # System-level configuration files
└── docker-compose.yml  # Docker configuration for development
```

## Frontend Structure (Next.js)

```
frontend/
├── app/                # Next.js App Router pages and layouts
│   ├── (auth)/         # Authentication-related pages (grouped route)
│   ├── (dashboard)/    # Protected dashboard routes (grouped route)
│   ├── api/            # API routes (Next.js API handlers)
│   ├── layout.tsx      # Root layout
│   └── page.tsx        # Home page
├── components/         # React components
│   ├── ui/             # Shadcn UI components
│   └── shared/         # Custom shared components
├── hooks/              # Custom React hooks
├── lib/                # Utility functions and configuration
│   ├── env.ts          # Type-safe environment variables
│   └── utils.ts        # Helper functions
├── public/             # Static assets
└── styles/             # Global styles
```

## Backend Structure (FastAPI)

```
backend/
├── alembic/            # Database migration scripts
├── app/                # Main application package
│   ├── api/            # API endpoints
│   │   ├── v1/         # API version 1
│   │   │   ├── endpoints/  # Resource-specific endpoints
│   │   │   └── router.py   # API router
│   │   └── auth/       # Authentication endpoints
│   ├── config/         # Configuration settings
│   ├── crud/           # Database CRUD operations
│   ├── db/             # Database setup and session
│   ├── models/         # SQLAlchemy ORM models
│   └── schemas/        # Pydantic schemas
├── scripts/            # Utility scripts
└── main.py             # Application entry point
```

## Architecture Patterns

### Frontend
- **App Router**: Next.js App Router for file-based routing
- **Server Components**: Leveraging React Server Components where appropriate
- **Client Components**: Using "use client" directive for interactive components
- **Component Hierarchy**: Following atomic design principles
- **Data Fetching**: Using TanStack Query for server state management

### Backend
- **Layered Architecture**:
  - API Layer: FastAPI routes and endpoints
  - Service Layer: Business logic
  - Data Access Layer: CRUD operations
- **Dependency Injection**: Using FastAPI's dependency system
- **Repository Pattern**: Abstracting database operations
- **Schema Validation**: Using Pydantic for request/response validation

## Naming Conventions

- **Files**: 
  - Frontend: kebab-case for components and utilities (e.g., `job-card.tsx`)
  - Backend: snake_case for Python files (e.g., `user_service.py`)
- **Components**: PascalCase for React components (e.g., `JobCard`)
- **Functions**: camelCase for JavaScript/TypeScript, snake_case for Python
- **Variables**: camelCase for JavaScript/TypeScript, snake_case for Python
- **Database**: snake_case for table and column names

## Import Conventions

- Group imports by:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- Sort imports alphabetically within each group