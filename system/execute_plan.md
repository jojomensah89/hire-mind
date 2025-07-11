# Execute `taskmaster-ai` Plan

This document outlines the process for Gemini to execute a `taskmaster-ai` generated plan.

## Execution Process:

1.  **Load and Understand the Plan:**
    *   Read the `tasks/tasks.json` file to understand all tasks, subtasks, dependencies, and requirements.
    *   Use `get_tasks` to list all tasks and `get_task` for detailed information on specific tasks.
    *   Ensure all needed context is available. If not, use `google_web_search` or `search_file_content` to gather more information.

2.  **Iterative Implementation:**
    *   Use `next_task` to identify the next task to work on based on dependencies and status.
    *   For each task:
        *   **Understand:** Read the task description and details thoroughly.
        *   **Plan (Internal):** Formulate a concise internal plan for implementing the task. This might involve identifying specific files to modify, functions to write, or tests to create.
        *   **Implement:** Use `read_file`, `write_file`, `replace`, and `run_shell_command` to implement the task. Adhere to existing project conventions and coding styles.
        *   **Verify (Local):** If applicable, run local tests or checks to ensure the task is correctly implemented. Use `run_shell_command` for this.
        *   **Update Status:** Once a task is completed and verified, update its status using `set_task_status` (e.g., `set_task_status(id='<task_id>', status='done', projectRoot='C:/Users/EbenezerMensah/Desktop/Test/project-guide/')`).

3.  **Validation Gates:**
    *   After completing a set of related tasks or a major feature, run the project's validation suite.
    *   Identify the correct commands for linting, type-checking, and running tests by examining `package.json`, `README.md`, or other configuration files.
    *   Example (if a `package.json` exists with `lint` and `test` scripts):
        ```
        default_api.run_shell_command(command='npm run lint && npm test', description='Run linting and tests to validate changes.')
        ```
    *   Fix any failures and re-run until all pass.

4.  **Completion and Reporting:**
    *   Once all tasks are completed and all validation gates pass, report completion status to the user.
    *   Provide a summary of the implemented features and any relevant instructions (e.g., how to run the application).

## Reference:

*   `taskmaster-ai` documentation: [Link to taskmaster-ai docs if available, otherwise mention it's an internal tool]
*   Project-specific conventions: [Mention where to find project conventions, e.g., `GEMINI.md`]
