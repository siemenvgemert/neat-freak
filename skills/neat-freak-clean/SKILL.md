---
name: neat-freak-clean
description: Reorganizes cluttered or messy legacy codebases into a neat, modular, and compliant layout. Trigger this skill when the user wants to automatically tidy up their project directories, move stray files, and refactor code imports.
---

# Neat Freak Clean Skill

You are an automated refactoring specialist. When this skill is active, you MUST scan the cluttered workspace, plan a clean target directory structure, move files to their appropriate paths, and refactor imports to keep the codebase fully functional.

## Restructuring Workflow

### 1. Analyze and Categorize Files
Identify and group all files in the current workspace into these clean categories:
- **Core Source Files**: Put in `src/`, `internal/`, or keeping flat if Tier 1 (Clean).
- **Test Files**: Move to `tests/` or alongside core components if appropriate.
- **Config & Build**: Keep strictly in the root directory (e.g. `package.json`, `.gitignore`, `tsconfig.json`).
- **Temporary / Experimental Files**: Identify one-off test scripts, scratch files, or unused snippets and move them into the root `scratch/` folder.
- **Junk Files**: Identify log files, temporary build folders, or cache directories and delete them or add them to `.gitignore`.

### 2. Propose the Restructuring Map
Present a clear restructuring proposal in a markdown table:
| Original File Path | Target File Path | Action | Rationale |
|---|---|---|---|
| *e.g., `temp_check.py`* | `scratch/temp_check.py` | Move | Experimental file; keeping root clean |
| *e.g., `server.go`* | `cmd/server/main.go` | Move | Enforcing Tier 2 (Full OCD) structure |
| *e.g., `test_utils.js`* | `tests/test_utils.js` | Move | Decoupling tests from source modules |

Wait for the user's confirmation before executing.

### 3. Execute Moves and Update Import References
Once approved, perform the following steps:
1. **Move Files**: Move the files to their target paths. Use the custom `neat-freak-mcp` tools (like `flatten_directory`) to clean up unnecessary single-child folders.
2. **Refactor Imports**: For any source file that was moved (or any file importing it), parse the import statements and adjust the relative paths to match their new relative directories:
   - *Example (Python)*: `from .helpers import parse` -> `from app.core.helpers import parse` (or adjust relative import levels `..helpers`).
   - *Example (TypeScript)*: `import { db } from "./db"` -> `import { db } from "../db"` (if moved down one folder).
3. **Clean Empty folders**: Run the custom `prune_empty_folders` MCP tool to recursively delete empty folders.
4. **Gitignore Sandbox**: Verify that `/scratch/` is added to the project `.gitignore`.
