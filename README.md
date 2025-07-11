# Hire-Mind

This project is a modern job board application that leverages AI to connect job seekers with relevant opportunities. The application is built with a Next.js frontend and a FastAPI backend.

## Project Overview

Hire-Mind provides a platform for employers to post job openings and for job seekers to search and apply for jobs. The key features include:

- **AI-powered job matching:** Utilizes AI to match job seekers with the most relevant job postings based on their skills and experience.
- **User authentication and billing:** Secure user authentication and subscription-based billing.

## Tech Stack

### Frontend

- **Framework:** Next.js
- **UI:** Shadcn UI
- **State Management:** TanStack Query
- **Authentication:** Clerk
- **Environment Variables:** @t3-oss/env-nextjs

### Backend

- **Framework:** FastAPI
- **Database:** SQLite (for development), PostgreSQL (for production)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Dependency Management:** uv

## Getting Started

### Prerequisites

- Node.js
- Python
- Docker (optional, for production deployment)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jojomensah89/hire-mind.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd hire-mind
   ```
3. **Install backend dependencies:**
   ```bash
   cd backend
   uv pip install -r requirements.txt
   ```
4. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the backend development server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
2. **Start the frontend development server:**
   ```bash
   cd ../frontend
   npm run dev
   ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.