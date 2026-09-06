# neat-freak

> **Obsessively organized, clean, and symmetrical codebase architectures optimized for human sanity and AI token economy.**

neat-freak is a developer plugin for agentic AI editors (compatible with Google Antigravity, Gemini-based agents, and Claude Code). It guides AI assistants to design minimalist directory structures, audit project directories for clutter, and optimize files to reduce search times and context token usage.

---

## Bundled Skills (Optimized for 1-Turn Execution with Gemini 3.8 Flash)

This plugin bundles **eight custom skills** that work together to maintain a clean codebase with zero unnecessary agent round-trips:

| Skill Trigger | Target Role | Description |
|---|---|---|
| neat-freak | **Scaffolding & Layouts** | Bootstraps clean, minimal workspace structures with zero-roundtrip inlined stack blueprints. |
| neat-freak-audit | **Workspace Clutter Audit** | Fast 1-turn audit using `os.scandir` checking empty dirs, nesting, and stray files with a 0-100 scorecard. |
| neat-freak-review | **Placement Review** | Evaluates new or modified files against placement rules in milliseconds before commits. |
| neat-freak-comfy | **AI Agent Token Optimizer** | Inspects git-ignores, nesting depth, and discoverability to minimize search hops and token costs. |
| neat-freak-debt | **Technical Layout Debt** | Instant harvester that compiles all neat-freak and ponytail layout simplification comments in `layout_debt.md`. |
| neat-freak-inspect | **Dependency Inspector** | Fast AST & regex analyzer detecting architectural coupling, circular dependencies, and layer violations. |
| neat-freak-clean | **Legacy Workspace Reorganizer** | Reorganizes cluttered codebases into a neat, modular layout with automated diagnostics. |
| neat-freak-help | **Quick Reference Card** | Renders a cheatsheet card detailing architecture tiers, guidelines, and command shortcuts. |

---

## Simplicity Tiers

neat-freak strictly enforces the rule: **"Build the absolute simplest layout that satisfies the current requirements."**

| Tier | Title | Target Scope | Structure Details |
|---|---|---|---|
| **Tier 0** | Low | Basic scripts & utilities | Single script or HTML file. No subfolders, no config files, standard libraries only. |
| **Tier 1** | Clean | Single packages | Flat directory. 1 configuration/dependency file, entry file, tests, and README. |
| **Tier 2** | Full OCD | Modular / Multi-person projects | Standard layouts (`src/`, `app/`, `internal/`) with cleanly decoupled configuration scopes (max depth 3). |

---

## Core Design Principles

1. **YAGNI (You Aren't Gonna Need It)**: Do not generate directories, boilerplates, or abstractions unless an active requirement demands them.
2. **Favor Standard Libraries & Native Features**: Avoid importing external libraries and packages if a standard system library or native platform API satisfies the job.
3. **Symmetry & Clutter-Free**: No source code files sit in root (except for Tier 0/1 entry points). Keep nesting depths below 4 levels (3 in OCD mode).
4. **ponytail: Documentation**: Mark any intentional structural or functional simplifications with code comments so other developers (and agents) understand the choice:
   - `// ponytail: simplified router using standard multiplexer to avoid framework boilerplate`
   - `# ponytail: using sqlite inline queries to avoid SQL-Alchemy setup overhead`
5. **Multi-Agent Isolation**: If multiple AI subagents run concurrently, they must write all temporary executions and scratch scripts inside role-isolated subdirectories inside `scratch/` (e.g. `scratch/researcher/`, `scratch/coder/`) to avoid context cross-talk and file locks.
6. **File Naming Conventions**: All created files must follow clean, stack-idiomatic casing: `snake_case` for Python/Rust, `kebab-case` for TS/JS/HTML/CSS (except PascalCase React components), and lowercase single words for Go. Generic names (like `helper.js`) or repeating the parent directory's name (like `models/user_model.py`) are strictly prohibited.

---

## High-Speed Python CLI Helpers (Python 3.8+ / Zero-Dependency)

The plugin provides high-performance standalone scripts in `scripts/` that run in under 30ms with zero pip dependencies:

- **`audit_workspace.py`**: High-speed recursive workspace auditor using `os.scandir`.
  ```bash
  python scripts/audit_workspace.py [--json]
  ```
- **`harvest_debt.py`**: Instant ponytail comment harvester.
  ```bash
  python scripts/harvest_debt.py [-w/--write]
  ```
- **`inspect_deps.py`**: AST and regex import scanner detecting circular loops and layer violations.
  ```bash
  python scripts/inspect_deps.py
  ```
- **`pre_commit_check.py`**: Fast placement and nesting depth validator for Git or working tree.
  ```bash
  python scripts/pre_commit_check.py --table --working-tree
  ```

---

## Custom MCP Tools (`neat_freak_mcp.py`)

The bundled Model Context Protocol (MCP) server exposes 8 high-level tools directly to AI agents:

- **`audit_workspace`**: Runs the instant cleanliness audit and returns the complete scorecard in 1 turn.
- **`harvest_debt`**: Scans and compiles `layout_debt.md` in milliseconds.
- **`inspect_dependencies`**: Builds the import graph and detects circular dependencies in milliseconds.
- **`review_layout`**: Evaluates modified or staged files against neat-freak rules.
- **`flatten_directory`**: Moves all files in a single-child nested directory up and deletes the empty parent folder.
- **`prune_empty_folders`**: Recursively deletes all empty directories in the workspace using high-speed traversal.
- **`clear_scratch_directory`**: Deletes all files and folders inside `scratch/` to clean up experimental code.
- **`clear_agent_sandbox`**: Deletes a specific agent's isolated subfolder inside `scratch/`.

To enable this server, configure it in your `mcp_config.json`.

---

## Git Pre-Commit Hook

To prevent cluttered code layouts from being committed, install the layout-checking pre-commit hook:

1. **Check Description**: It automatically evaluates staged files before a commit is completed. If any source code files sit in root or nesting depth exceeds limits, it blocks the commit.
2. **Installation**:
   ```bash
   ./scripts/install-hook.sh
   ```

---

## Plugin Structure

```text
neat-freak/
├── plugin.json               # Plugin registration configuration
├── plugin.yaml               # Metadata list of skills and triggers
├── mcp_config.json           # Custom MCP server configuration
├── README.md                 # This documentation
├── mcp/
│   └── neat_freak_mcp.py     # High-speed 8-tool Python MCP server script
├── scripts/
│   ├── audit_workspace.py    # High-speed workspace cleanliness auditor
│   ├── harvest_debt.py       # Instant ponytail debt harvester
│   ├── inspect_deps.py       # AST & regex circular import analyzer
│   ├── pre_commit_check.py   # Pre-commit & layout reviewer
│   ├── pre-commit.template   # Shell hook template
│   └── install-hook.sh       # Hook installer bash script
└── skills/
    ├── neat-freak/           # Main Scaffolding Skill (with inlined fast-path blueprints)
    ├── neat-freak-audit/     # Cleanliness Audit Skill (1-turn execution)
    ├── neat-freak-review/    # Pull Request / Diff Review Skill
    ├── neat-freak-comfy/     # AI Optimization Skill
    ├── neat-freak-debt/      # Technical Layout Debt Skill
    ├── neat-freak-inspect/   # Dependency Inspector Skill
    ├── neat-freak-clean/     # Legacy Workspace Reorganizer
    └── neat-freak-help/      # Quick Reference Cheatsheet
```

---

## Intensity Modes

You can dynamically toggle the plugin's intensity levels or configure default modes:

- **`neat-freak off`**: Completely deactivates all layout checking.
- **`neat-freak on`** (Default): Enforces standard layout guidelines (Tiers 0 and 1, max nesting depth 4).
- **`neat-freak ocd`**: Enforces strict modular layout symmetry (Tier 2 / Full OCD, max nesting depth 3).

### Configuration Priority
1. **Environment Variable**: `NEAT_FREAK_DEFAULT_MODE` (`off`, `on`, `ocd`).
2. **Local Configuration File**: `.neat-freak-config.json` placed in root containing `{"defaultMode": "on"}`.
3. **Global Configuration File**: `~/.config/neat-freak/config.json` containing `{"defaultMode": "on"}`.
