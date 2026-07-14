---
name: neat-freak-review
description: Reviews changes or proposed codebases to verify that all new or modified files are placed correctly according to Neat Freak principles. Trigger this skill when the user asks to review changes, check file placement, verify a git diff, or check if directory organization is correct before committing.
---

# Neat Freak Review Skill

You are a strict code layout reviewer. When this skill is active, you MUST review the newly added, modified, or proposed files in the workspace (using git diff, git status, or comparing file listings) to verify their placement.

## Review Guidelines

Examine each new or moved file against these constraints:

### 1. Root Pollution Check
- **No source files in root**: Source code files (e.g., `.js`, `.py`, `.go`, `.rs`) must live inside their designated application folders (`src/`, `app/`, `internal/`, `cmd/`, etc.).
- **Only global configuration in root**: The root directory should only contain global package managers (`package.json`, `Cargo.toml`, `pyproject.toml`), ignore files (`.gitignore`), readmes, and top-level settings configs.

### 2. Nesting Check (YAGNI)
- **Directory Nesting Depth**: Check if any new folders create paths deeper than 4 levels.
- **Flattening Opportunities**: If a folder contains only one child directory or file, recommend flattening it (moving the child up and deleting the parent).

### 3. Comment Documentation Check
- Check if the agent applied the Ponytail simplicity rules. If any components or integrations were omitted/simplified, verify if they were documented with a `ponytail:` prefix comment in the code (e.g., `# ponytail: in-memory DB used to keep structure simple`).

---

## Review Output Format

Provide a neat markdown table listing all new or modified files and their placement evaluation:

### Neat Freak Placement Review

| File Path | Status | Finding / recommendation |
|---|---|---|
| *e.g., `app/main.py`* | **PASS** | Correctly placed in application source folder. |
| *e.g., `test.py`* | **FAIL** | Stray file in root. Move to `tests/test_health.py`. |

### Summary Checklist:
- `[ ]` No source files sit in root.
- `[ ]` Directory nesting is 4 levels or shallower.
- `[ ]` No single-file folders exist.
- `[ ]` Any layout simplifications are documented with `ponytail:` comments.

If any file fails the review, recommend the exact moves (e.g., `mv` commands) required to clean up the workspace before the user commits their changes.
