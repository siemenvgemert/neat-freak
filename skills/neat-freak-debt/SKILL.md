---
name: neat-freak-debt
description: Scans the codebase to harvest and document all neat-freak and ponytail layout simplification comments, compiling them into a structured tracking ledger. Trigger this skill when the user wants to audit their technical layout debt or view simplified shortcuts.
---

# Neat Freak Debt Skill

You are a technical debt inspector. When this skill is active, you MUST scan the source code of the project workspace to identify and compile all comments documenting simplified layout choices.

## Workflow

### 1. Scan for Comments
Scan all source files in the workspace (excluding build folders and dependencies like `node_modules/`, `target/`, `.venv/`) for comments matching these pattern markers:
- `// ponytail:` / `# ponytail:`
- `// neat-freak:` / `# neat-freak:`

Extract:
- The path of the file containing the comment.
- The line number of the comment.
- The text content describing the simplification choice.

### 2. Generate the Layout Debt Ledger
Compile the results into a file named `layout_debt.md` at the root of the workspace directory. Use the following markdown structure:

```markdown
# Layout Debt Ledger

This file tracks all intentional architecture and implementation simplifications in the codebase.

## Staged Simplifications

| File Path | Line | Description |
|---|---|---|
| *e.g., `app.py`* | 12 | using standard library http.server to avoid external dependencies |
| *e.g., `main.go`* | 45 | inline sql query used to bypass ORM boilerplate setup |
```

If no layout debt comments are found, document that the codebase has zero recorded layout simplification debt.
