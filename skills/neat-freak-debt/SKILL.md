---
name: neat-freak-debt
description: Scans codebase for ponytail and neat-freak simplification comments, compiling a Layout Debt Ledger (layout_debt.md).
---

# Neat Freak Debt Skill

You are a technical debt inspector. When this skill is active, you MUST scan the source code of the project workspace to identify and compile all comments documenting simplified layout choices.

## Fast-Path Execution (1-Turn)

### 1. Run the Layout Debt Harvester
Execute the dedicated high-speed debt harvester:
- **CLI Fast-Path (Recommended)**: Run `python ~/.gemini/config/plugins/neat-freak/scripts/harvest_debt.py --write`
- **MCP Fast-Path**: Call `harvest_debt(workspace_path="...", write_file=True)`

The script scans all workspace source files in milliseconds for:
- `// ponytail:` / `# ponytail:` / `/* ponytail:`
- `// neat-freak:` / `# neat-freak:`

### 2. Output and Ledger File
The harvester extracts the file path, line number, and simplification rationale, automatically creating or updating `layout_debt.md` in the root of the workspace:

```markdown
# Layout Debt Ledger

This file tracks all intentional architecture and implementation simplifications in the codebase.

## Staged Simplifications

| File Path | Line | Description |
|---|---|---|
| `app.py` | 12 | using standard library http.server to avoid external dependencies |
```

If zero comments are found, it records that the codebase has zero recorded layout simplification debt. Present the ledger summary directly to the user.
