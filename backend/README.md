# Job Board AI Backend

This is the backend for the Job Board AI application, built with FastAPI.

## Setup

1.  **Environment Variables**: Create a `.env` file based on `.env.example` and set the following:
    
    *   `DATABASE_URL`: Your database connection string (e.g., `sqlite:///./test.db` or `postgresql://user:password@host:port/dbname`).

2.  **Install Dependencies** (using uv ):
    ```bash
    uv install
    ```

3.  **Run Migrations**:
    ```bash
    alembic upgrade head
    ```

4.  **Run the Application**:

    *   **Development Server**:
        ```bash
        fastapi dev main.py
        ```
    *   **Production Server** :
        ```bash
        fastapi run main.py
        ```

## Development

### Running Tests

```bash
pytest app/tests
```
