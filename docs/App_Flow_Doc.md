# Application Flow

This document outlines the user flow for the AI Job Board application.

## User Authentication Flow (Clerk)

1.  A user visits the site and clicks "Sign Up" or "Log In".
2.  The Clerk authentication modal appears.
3.  The user signs up or logs in using their email, password, or a social provider.
4.  Upon successful authentication, the user is redirected to the main job board.

## Job Seeker Flow

1.  The user lands on the main page, which displays a list of recent job postings.
2.  The user can use the search bar and filters (e.g., location, job type) to find relevant jobs.
3.  The system displays AI-powered job recommendations based on the user's profile and activity.
4.  The user clicks on a job posting to view the full details.
5.  The user clicks the "Apply" button, which may redirect them to an external application link or open an application form.

## Employer/Recruiter Flow

1.  An employer user navigates to the "Post a Job" section.
2.  **Billing (Clerk):**
    *   If the employer is on a free plan or has exhausted their job posting limit, they are prompted to upgrade to a paid plan.
    *   Clerk's billing pages handle the subscription and payment process.
3.  The employer fills out a form with the job details (title, description, location, etc.).
4.  The employer submits the form to create the new job posting.
5.  The employer can view, edit, or delete their active job postings from their dashboard.
