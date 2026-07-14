---
name: neat-freak-help
description: Displays a quick reference card and cheatsheet for the neat-freak plugin, detailing the three simplicity tiers, file organization principles, and available skills. Trigger this skill when the user asks for help or commands related to neat-freak.
---

# Neat Freak Help Skill

When this skill is active, you MUST render a beautifully formatted quick-reference cheat sheet summarizing the Neat Freak design system.

## Cheat Sheet Content

Renders the following quick reference card directly to the user:

### Neat Freak Cheat Sheet

#### 1. Available Custom Skills
- **`neat-freak`**: Bootstraps neat, minimalist workspace structures using stack reference templates.
- **`neat-freak-audit`**: Checks the workspace for empty folders, deep nesting, and clutter, and generates a scorecard.
- **`neat-freak-review`**: Evaluates new/modified files to check if they conform to the folder guidelines.
- **`neat-freak-comfy`**: Audits the repository layout to optimize search speed and minimize token costs for AI agents.
- **`neat-freak-debt`**: Scans the codebase to harvest and document all neat-freak and ponytail layout simplification comments in `layout_debt.md`.
- **`neat-freak-inspect`**: Scans import statements and dependencies to check for architectural coupling, circular dependencies, or layer violations.
- **`neat-freak-clean`**: Reorganizes cluttered or messy legacy codebases into a neat, modular, and compliant layout.
- **`neat-freak-help`**: Shows this quick reference card.

#### 2. Architecture Simplicity Tiers
Always build the simplest structure that satisfies the current requirements:
| Tier | Title | Target Scope | Structure Details |
|---|---|---|---|
| **Tier 0** | Low | Simple scripts / Single pages | Single file, no config, standard libraries only. |
| **Tier 1** | Clean | Single package / Flat structures | Single directory, 1 config file, entry + tests + README. |
| **Tier 2** | Full OCD | Modular / Multi-person projects | Standard directories (`src/`, `internal/`), split config. |

#### 3. Core Organization Principles
- **YAGNI (You Aren't Gonna Need It):** Never create directories or boilerplate without an active requirement.
- **`ponytail:` Comments:** Document any intentional code/library simplifications with a code comment:
  - `// ponytail: simplified DB using inline query to avoid ORM boilerplate`
  - `# ponytail: using standard http.server to avoid external dependencies`
- **Symmetry & Clutter-Free**: Avoid files in root except config and README. Keep nesting paths below 4 levels.
- **Multi-Agent Isolation**: If multiple AI subagents run concurrently, they must write all temporary executions and scratch scripts inside role-isolated subdirectories inside `scratch/` (e.g. `scratch/researcher/`, `scratch/coder/`).
- **File Naming Conventions**: Files must follow idiomatic naming casing: `snake_case` for Python/Rust, `kebab-case` for TS/JS/HTML/CSS (except PascalCase React components), and lowercase single words for Go. No redundant names (e.g. `models/user.py` not `models/user_model.py`).

#### 4. Intensity Modes
Toggle the plugin intensity level dynamically or configure defaults:
- **neat-freak off**: Deactivates all layout checks and allows any file structure.
- **neat-freak on** (Default): Enforces standard layout guidelines (Tiers 0 and 1).
- **neat-freak ocd**: Enforces strict modular layout symmetry (Tier 2).

Configuration Resolution Order:
1. Environment Variable: `NEAT_FREAK_DEFAULT_MODE` (off | on | ocd)
2. Local Config file: `.neat-freak-config.json` at root containing `{"defaultMode": "on"}`
3. Global Config file: `~/.config/neat-freak/config.json` containing `{"defaultMode": "on"}`

