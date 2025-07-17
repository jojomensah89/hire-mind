# Technology Stack & Build System

## Frontend
- **Framework**: Next.js 15.x with React 19
- **UI Components**: Shadcn UI (built on Radix UI)
- **Styling**: Tailwind CSS 4.x
- **State Management**: TanStack Query 5.x
- **Authentication**: Clerk
- **Environment Variables**: @t3-oss/env-nextjs
- **Form Handling**: React Hook Form with Zod validation
- **Code Quality**: Biome for linting and formatting

## Backend
- **Framework**: FastAPI
- **Database**: 
  - Development: SQLite
  - Production: PostgreSQL 13
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Dependency Management**: uv (Python package manager)
- **Authentication**: Clerk (via webhooks)

## Infrastructure
- **Containerization**: Docker
- **Database**: PostgreSQL 13 (in production)

## Common Commands

### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Lint code
npm run lint
```

### Backend
```bash
# Setup virtual environment
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/MacOS

# Install dependencies
uv sync

# Run development server
fastapi dev main.py

# Run tests
pytest

# Generate migrations
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Docker
```bash
# Start PostgreSQL database
docker-compose up -d

# Stop services
docker-compose down
```

## Code Style & Conventions

### Frontend
- Use TypeScript for all new code
- Follow Biome linting rules
- Use functional components with hooks
- Organize components using atomic design principles
- Use TanStack Query for server state management
- Format code with Ultracite before committing (handled by husky pre-commit hook)

### Backend
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Organize code by domain (jobs, users, etc.)
- Use dependency injection for services
- Write tests for all API endpoints