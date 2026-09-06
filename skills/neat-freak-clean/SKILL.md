---
name: neat-freak-clean
description: Reorganizes cluttered codebases into clean layouts, moving stray files, updating imports, and pruning empty folders.
---

# Neat Freak Clean Skill

You are an automated refactoring specialist. When this skill is active, you MUST scan the cluttered workspace, plan a clean target directory structure, move files to their appropriate paths, and refactor imports to keep the codebase fully functional.

## Restructuring Workflow

### 1. Rapid Diagnosis
Run `python ~/.gemini/config/plugins/neat-freak/scripts/audit_workspace.py` (or MCP `audit_workspace`) to immediately identify all stray root files, unignored artifacts, and empty or single-child directories.

Group workspace files into:
- **Core Source Files**: Place in `src/`, `internal/`, or keep flat if Tier 1.
- **Test Files**: Move to `tests/` or alongside core components if appropriate.
- **Config & Build**: Keep in root (`package.json`, `.gitignore`, `tsconfig.json`, `pyproject.toml`).
- **Temporary / Experimental Files**: Move scratch scripts and one-off snippets into `scratch/`.
- **Junk Files**: Add cache/build directories to `.gitignore`.

### 2. Propose the Restructuring Map
Present a clear restructuring proposal in a markdown table:
| Original File Path | Target File Path | Action | Rationale |
|---|---|---|---|
| *e.g., `temp_check.py`* | `scratch/temp_check.py` | Move | Experimental file; keeping root clean |
| *e.g., `server.go`* | `cmd/server/main.go` | Move | Enforcing Tier 2 structure |

Wait for user confirmation before executing moves.

### 3. Execute Moves and Update Import References
Once approved:
1. **Move Files**: Move the files to their target paths. Use the custom `flatten_directory` MCP tool or shell `mv` commands.
2. **Refactor Imports**: For any source file moved, adjust relative import paths (`from ..core import ...`).
3. **Prune Empty Folders**: Run the custom `prune_empty_folders` MCP tool or `audit_workspace.py` to recursively clean empty directories.
4. **Gitignore Sandbox**: Verify `/scratch/` is added to `.gitignore`.
