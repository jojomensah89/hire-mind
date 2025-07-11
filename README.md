# AI Job Board

This project is a modern job board application that leverages AI to connect job seekers with relevant opportunities. The application is built with a Next.js frontend and a FastAPI backend.

## Project Overview

The AI Job Board provides a platform for employers to post job openings and for job seekers to search and apply for jobs. The key features include:

- **AI-powered job matching:** Utilizes AI to match job seekers with the most relevant job postings based on their skills and experience.
- **User authentication and billing:** Secure user authentication and subscription-based billing are handled by Clerk.
- **Environment variable management:** Type-safe environment variable management is implemented using `@t3-oss/env-nextjs`.

## Tech Stack

### Frontend

- **Framework:** Next.js
- **UI:** Shadcn UI
- **State Management:** TanStack Query
- **Authentication:** Clerk
- **Environment Variables:** @t3-oss/env-nextjs

### Backend

- **Framework:** FastAPI
- **Database:** PostgreSQL (via Docker)

## Getting Started

### Prerequisites

- Node.js
- Python
- Docker

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/job-board-ai.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd job-board-ai
   ```
3. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```
4. **Install backend dependencies:**
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```
5. **Start the development servers:**
   - **Frontend:** `npm run dev`
   - **Backend:** `uvicorn main:app --reload`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.
