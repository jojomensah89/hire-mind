# Hire-Mind Product Requirements Document (PRD)

## 1. Introduction

Hire-Mind is an AI-powered job board application designed to efficiently connect job seekers with relevant employment opportunities and provide employers with tools to manage their job postings and applications. This document outlines the core features, user flows, and technical architecture of the Hire-Mind platform.

## 2. Goals

*   To provide a seamless and intuitive experience for job seekers to discover and apply for jobs.
*   To empower employers with robust tools for posting, managing, and tracking job applications.
*   To leverage Artificial Intelligence for intelligent job matching and resume summarization.
*   To ensure a scalable, maintainable, and secure platform.

## 3. Target Audience

*   **Job Seekers:** Individuals actively looking for employment, seeking personalized job recommendations and an easy application process.
*   **Employers/Recruiters:** Organizations and individuals looking to post job openings, manage applicants, and find suitable candidates.

## 4. Key Features

### 4.1. User Management & Authentication

*   **User Registration & Login:** Users (job seekers and employers) can sign up and log in using email/password or social providers.
*   **User Profiles:** Management of user-specific information.
*   **Organization Management:** Employers can create and manage organizations.
*   **Role-Based Access Control:** Differentiate between job seeker and employer functionalities.

### 4.2. Job Seeker Features

*   **Job Board:** Browse and view a list of recent job postings.
*   **Job Search & Filtering:** Search for jobs by keywords, location (city, state), experience level, and job type.
*   **AI-Powered Job Matching/Recommendations:** Receive personalized job recommendations based on profile and activity.
*   **Job Details View:** View comprehensive details of a job posting.
*   **Job Application:** Apply for jobs directly through the platform (requires an account and uploaded resume).
*   **Resume Management:** Upload and manage resumes.
*   **AI Resume Summary:** Automatically generate an AI summary of the uploaded resume for employers.
*   **Notification Settings:** Configure email notifications for new job listings.

### 4.3. Employer Features

*   **Job Posting Creation:** Create new job listings with detailed information (title, description, location, wage, experience, type).
*   **Job Posting Management:** View, edit, and delete active job postings.
*   **Job Application Tracking:** View applications for their job postings.
*   **Application Ranking:** AI-powered ranking of job applications.
*   **Notification Settings:** Configure email notifications for new job applications.
*   **Employer Dashboard:** Centralized view for managing job listings and applications.

### 4.4. AI Features

*   **AI Job Matching:** Intelligent algorithms to connect job seekers with relevant jobs.
*   **AI Resume Summarization:** Generate concise summaries of job seeker resumes for employers.
*   **AI Application Ranking:** Rank job applications based on relevance to the job description.
*   **AI Search:** Dedicated AI search functionality for job seekers (requires authentication).

### 4.5. Notifications & Emails

*   **Daily Job Listing Notifications:** Job seekers receive daily email digests of new job listings matching their preferences.
*   **Daily Application Notifications:** Employers receive daily email digests of new applications for their job postings.

### 4.6. Billing & Subscriptions

*   **Subscription Plans:** Employers can subscribe to different plans to unlock job posting limits and other premium features.
*   **Payment Processing:** Integration with a payment gateway (handled by Clerk).

## 5. User Flows

### 5.1. User Authentication Flow

1.  User visits the site and selects "Sign Up" or "Log In".
2.  Clerk authentication modal/page appears.
3.  User authenticates (email/password, social provider).
4.  Upon success, user is redirected to the main job board (job seeker) or organization selection/employer dashboard (employer).

### 5.2. Job Seeker Flow

1.  User lands on the main page, sees recent job postings.
2.  User searches/filters jobs or views AI recommendations.
3.  User clicks on a job posting to view details.
4.  User clicks "Apply":
    *   If not authenticated, prompted to sign up/log in.
    *   If authenticated but no resume, prompted to upload resume.
    *   If authenticated with resume, application form opens/redirects to external link.
5.  User can manage notification settings and resume in their user settings.

### 5.3. Employer/Recruiter Flow

1.  Employer navigates to "Post a Job" section.
2.  **Billing Check:** If limits are reached or no active plan, prompted to upgrade/subscribe via Clerk's billing pages.
3.  Employer fills out job details form.
4.  Employer submits form to create job posting.
5.  Employer can view, edit, or delete job postings from their dashboard.
6.  Employer can view and manage applications for their job listings.

## 6. Technical Architecture

Hire-Mind is structured as a monorepo with distinct frontend and backend services, leveraging a modern tech stack for scalability and maintainability.

### 6.1. Overall Monorepo Structure

*   **Root:** Contains shared configurations (`.gitignore`, `docker-compose.yml`, `README.md`).
*   **`backend/`:** Houses the FastAPI application.
*   **`frontend/`:** Contains the Next.js application.
*   **`docs/`:** Project documentation.
*   **`system/`:** System-level documentation/scripts.

### 6.2. Frontend Stack

*   **Framework:** Next.js (React)
*   **UI Library:** Shadcn UI (built on Radix UI and Tailwind CSS)
*   **State Management:** TanStack Query (for server state)
*   **Authentication Integration:** Clerk (via `@clerk/nextjs`)
*   **Environment Variables:** `@t3-oss/env-nextjs` (type-safe management)
*   **Markdown Rendering:** `@mdxeditor/editor`, `next-mdx-remote`, `remark-gfm`
*   **File Uploads:** `@uploadthing/react`
*   **Email Components:** `@react-email/components`

### 6.3. Backend Stack

*   **Framework:** FastAPI (Python)
*   **ORM:** SQLAlchemy
*   **Migrations:** Alembic
*   **Dependency Management:** `uv`
*   **Testing:** Pytest

### 6.4. Database

*   **Development:** SQLite (`job-board.db`)
*   **Production:** PostgreSQL (managed via Docker)

### 6.5. Authentication

*   **Provider:** Clerk (handles user authentication, organization management, and billing).
*   **Integration:** Clerk webhooks and APIs are used to synchronize user/organization data with the backend.

### 6.6. Background Processing & Event-Driven Architecture

*   **Platform:** Inngest
*   **Functions:**
    *   Clerk webhook handlers (user/organization creation, update, deletion).
    *   AI summary generation for uploaded resumes.
    *   Job application ranking.
    *   Daily email notification preparation and sending.

### 6.7. File Storage

*   **Service:** Uploadthing (for resume uploads).

### 6.8. Email Service

*   **Service:** Resend (for sending transactional and notification emails).

### 6.9. Deployment

*   **Containerization:** Docker (using `docker-compose.yml` for local development and potentially for production).

## 7. Future Considerations

*   Advanced AI features (e.g., personalized job alerts, interview preparation).
*   Integration with external HR systems.
*   More detailed analytics for employers.
*   Mobile application development.
