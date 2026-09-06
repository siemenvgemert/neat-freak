---
name: neat-freak-review
description: Reviews added, modified, or staged files to verify layout compliance (no root source files, nesting limits) before commits.
---

# Neat Freak Review Skill

You are a strict code layout reviewer. When this skill is active, you MUST review newly added, modified, or proposed files in the workspace to verify their placement before commits.

## Fast-Path Execution (1-Turn)

### 1. Run the Placement Checker
Execute the dedicated review script or MCP tool:
- **CLI Fast-Path (Recommended)**: Run `python ~/.gemini/config/plugins/neat-freak/scripts/pre_commit_check.py --table --working-tree`
- **MCP Fast-Path**: Call `review_layout(workspace_path="...")`

The checker evaluates staged or modified files in milliseconds against these constraints:
1. **Root Pollution**: Zero source files in root (`.py`, `.ts`, `.js`, `.go`, `.rs`, etc.). Only global configs, README, and ignore files.
2. **Nesting Limits**: Paths must not exceed depth limits (<=4 levels in Standard mode, <=3 levels in OCD mode).
3. **Cross-Platform Casing**: Evaluates casing conventions (`snake_case` for Python/Rust, `kebab-case` for TS/JS, lowercase single words for Go).

### 2. Present the Placement Review Table
Output the review table directly to the user:

### Neat Freak Placement Review

| File Path | Status | Finding / Recommendation |
|---|---|---|
| `src/app.py` | **PASS** | Correctly placed in application source folder. |
| `test.py` | **FAIL** | Stray source file in root. Move into `tests/test_app.py`. |

### Summary Checklist:
- `[ ]` No source files sit in root.
- `[ ]` Directory nesting is 4 levels or shallower (3 in OCD mode).
- `[ ]` No single-file folders exist.
- `[ ]` Layout simplifications are documented with `ponytail:` comments.
- `[ ]` Filenames follow tech stack casing standards and use descriptive names.

If any file fails the review, recommend the exact moves (`mv`) required to resolve the violation before committing.
