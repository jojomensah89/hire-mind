# Project Folder Structure Guidelines

This document outlines the recommended folder structure for projects, promoting consistency, clarity, and ease of navigation for both human developers and AI agents like Gemini.

## Core Structure

```
.
├── .git/                 # Git version control
├── .github/              # GitHub specific configurations (e.g., workflows, issue templates)
├── .vscode/              # VS Code specific settings (e.g., launch.json, settings.json)
├── docs/                 # Project documentation (e.g., architecture, design, API docs)
├── src/                  # Source code
│   ├── main/             # Main application logic
│   └── tests/            # Unit and integration tests
├── templates/            # Reusable templates or boilerplate files
├── .gitignore            # Files and directories to be ignored by Git
├── package.json          # Node.js project metadata and dependencies
├── README.md             # Project overview and setup instructions
├── LICENSE               # Project license
└── ...                   # Other project-specific files (e.g., config files, build scripts)
```

## Directory Breakdown

### `.git/`
Contains Git's internal data for version control. You typically won't interact with this directly.

### `.github/`
Holds configurations related to GitHub, such as:
- `workflows/`: GitHub Actions workflows for CI/CD.
- `ISSUE_TEMPLATE/`: Templates for new issues.
- `PULL_REQUEST_TEMPLATE.md`: Template for pull request descriptions.

### `.vscode/`
Contains workspace-specific settings for VS Code. This can include:
- `settings.json`: Workspace settings.
- `extensions.json`: Recommended extensions.
- `launch.json`: Debugging configurations.

### `docs/`
Dedicated to project documentation. This can include:
- `architecture.md`: High-level system architecture.
- `api.md`: API documentation.
- `setup.md`: Detailed setup instructions.
- `decisions/`: Architecture Decision Records (ADRs).

### `src/`
The primary directory for all source code.
- `main/`: Contains the main application logic. For a CLI tool, this would be where the core command parsing and execution resides.
- `tests/`: Houses all unit and integration tests, mirroring the structure of `src/main`.

### `templates/`
(Specific to this `project-guide` tool)
Contains the various markdown templates that this CLI tool distributes. Each template should be a self-contained document.

### `.gitignore`
Specifies intentionally untracked files that Git should ignore.

### `package.json` (or equivalent for other languages)
For Node.js projects, this file defines project metadata, scripts, and dependencies.

### `README.md`
The main entry point for understanding the project. It should provide a clear overview, setup instructions, and usage examples.

### `LICENSE`
Specifies the licensing terms for the project.

## Naming Conventions

- **Directories:** Use `kebab-case` (e.g., `my-feature`, `user-management`).
- **Files:** Use `kebab-case` for general files (e.g., `my-component.js`, `data-utils.ts`). For classes or main entry points, `PascalCase` might be appropriate (e.g., `App.js`, `Main.java`).
- **Test Files:** Should be named `[original-file-name].test.[ext]` or `[original-file-name].spec.[ext]` (e.g., `user-service.test.js`).

## Modularity and Refactoring

- **Keep files concise:** Aim for files under 500 lines of code. Refactor larger files into smaller, more focused modules.
- **Group by feature:** Organize code into modules based on features or responsibilities rather than just type (e.g., `user/` containing `user.controller.js`, `user.service.js`, `user.model.js`).

This structure provides a clear, maintainable, and scalable foundation for projects, making it easier for both human developers and AI agents to navigate and contribute effectively.