---
name: neat-freak-audit
description: Audits workspace for messy structures, empty folders, stray files, and excessive nesting. Returns a 0-100 Cleanliness Scorecard.
---

# Neat Freak Audit Skill

You are a meticulous auditor specialized in maintaining neat, clutter-free, and highly organized repositories. When this skill is active, you MUST follow this fast 1-turn workflow to generate a Cleanliness Scorecard.

## Fast-Path Execution (1-Turn)

### 1. Run the Workspace Auditor
Execute the dedicated high-speed audit script or MCP tool:
- **CLI Fast-Path (Recommended)**: Run `python ~/.gemini/config/plugins/neat-freak/scripts/audit_workspace.py` (or relative path to workspace).
- **MCP Fast-Path**: Call `audit_workspace(workspace_path="...")`.

The script traverses the workspace using high-speed `os.scandir` in under 30ms and evaluates:
- **Empty Directories**: Identifies folders with zero files.
- **Single-Item Folders**: Detects unnecessary single-child folders that should be flattened.
- **Excessive Nesting**: Verifies nesting paths stay within limits (<=4 in Standard mode, <=3 in OCD mode).
- **Stray Root Files**: Detects source code files placed in the root directory.
- **Unignored Build Artifacts**: Checks for cache/build directories missing from `.gitignore`.
- **Boilerplate Duplication**: Detects redundant nested config files.

### 2. Present the Cleanliness Scorecard
Present the output returned by the auditor directly to the user:

#### A. Cleanliness Score & Rating
- **90-100 (Immaculate)**: Symmetrical, minimal nesting, zero empty folders, zero stray files.
- **70-89 (Neat but Expandable)**: Minor single-child folders or easily resolved clutter.
- **Below 70 (Cluttered)**: Multiple empty folders, deep nesting, missing `.gitignore` rules, or misplaced files.

#### B. Identified Structural Issues Table
| Issue Type | File/Folder Path | Description | Recommended Action |
|---|---|---|---|
| *e.g., Stray File* | `app.py` | Sits directly in root | Move to `src/app.py` |

#### C. Prioritized Cleanup Action Plan
Present the recommended moves, flattens, or deletions. Always confirm with the user before executing destructive file operations.
