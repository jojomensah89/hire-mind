# Generate Plan from Idea

This document outlines the process for generating a `taskmaster-ai` plan from a user's idea, suitable for Gemini's execution.

## Process:

1.  **Understand the Idea:** Read the user's idea and any provided context thoroughly. Identify the core functionality, desired outcomes, and any constraints.

2.  **Codebase Analysis (if applicable):**
    *   Search for similar features or patterns in the existing codebase using `search_file_content` and `glob`.
    *   Identify relevant files that can serve as examples or need modification.
    *   Note existing conventions (coding style, testing patterns, architectural choices) to ensure consistency.

3.  **External Research (if needed):**
    *   If the idea involves new technologies or complex algorithms, use `google_web_search` to gather information.
    *   Prioritize official documentation, well-regarded tutorials, and established best practices.

4.  **Formulate a `taskmaster-ai` Prompt:**
    *   Based on the understanding and research, formulate a clear and concise prompt for `taskmaster-ai`.
    *   The prompt should describe the desired feature, reference relevant codebase examples (with absolute paths), and specify any external resources.
    *   Example prompt structure:
        ```
        "Create a plan to implement [FEATURE_NAME]. The implementation should follow the patterns in [ABSOLUTE_PATH_TO_EXAMPLE_FILE]. Consider [EXTERNAL_RESOURCE_URL] for [SPECIFIC_ASPECT]." 
        ```

5.  **Generate Tasks with `taskmaster-ai`:**
    *   Use the `parse_prd` tool with the formulated prompt to generate initial tasks. Set `numTasks` to a reasonable number (e.g., 10-20) based on the complexity of the idea.
    *   Example:
        ```
        default_api.parse_prd(projectRoot='C:/Users/EbenezerMensah/Desktop/Test/project-guide/', input='./ideas/[YOUR_IDEA_FILE].md', numTasks=15)
        ```

6.  **Review and Refine Tasks:**
    *   After `taskmaster-ai` generates the tasks, review them for clarity, completeness, and logical flow.
    *   If necessary, use `expand_task` to break down complex tasks into smaller subtasks.
    *   Use `update_task` or `update_subtask` to refine descriptions, add details, or adjust dependencies.

7.  **User Review:**
    *   Present the generated `taskmaster-ai` plan to the user for review and approval.
    *   Be prepared to explain the plan and make adjustments based on user feedback.

## Output:

The `taskmaster-ai` plan will be stored in `tasks/tasks.json` (default location).