# neat-freak

> **Obsessively organized, clean, and symmetrical codebase architectures optimized for human sanity and AI token economy.**

neat-freak is a developer plugin for agentic AI editors (compatible with Claude Code, Google Antigravity, and Gemini-based agents). It guides AI assistants to design minimalist directory structures, audit project directories for clutter, and optimize files to reduce search times and context token usage.

---

## Bundled Skills

This plugin bundles **eight separate custom skills** that work together to maintain a clean codebase:

| Skill Trigger | Target Role | Description |
|---|---|---|
| neat-freak | **Scaffolding & Layouts** | Bootstraps clean, minimal workspace structures from curated stack reference templates. |
| neat-freak-audit | **Workspace Clutter Audit** | Scans for empty directories, excessive nesting, and misplaced config files, outputting a scorecard. |
| neat-freak-review | **Placement Review** | Evaluates new or modified files (via git status/diffs) to verify they are placed correctly before commits. |
| neat-freak-comfy | **AI Agent Token Optimizer** | Inspects git-ignores, nesting depth, and discoverability to minimize search hops and token costs. |
| neat-freak-debt | **Technical Layout Debt** | Scans the codebase to harvest and document all neat-freak and ponytail layout simplification comments in `layout_debt.md`. |
| neat-freak-inspect | **Dependency Inspector** | Scans import statements and dependencies to check for architectural coupling, circular dependencies, or layer violations. |
| neat-freak-clean | **Legacy Workspace Reorganizer** | Reorganizes cluttered or messy legacy codebases into a neat, modular, and compliant layout. |
| neat-freak-help | **Quick Reference Card** | Renders a cheatsheet card detailing architecture tiers, guidelines, and command shortcuts. |

---

## Simplicity Tiers

neat-freak strictly enforces the rule: **"Build the absolute simplest layout that satisfies the current requirements."**

| Tier | Title | Target Scope | Structure Details |
|---|---|---|---|
| **Tier 0** | Low | Basic scripts & utilities | Single script or HTML file. No subfolders, no config files, standard libraries only. |
| **Tier 1** | Clean | Single packages | Flat directory. 1 configuration/dependency file, entry file, tests, and README. |
| **Tier 2** | Full OCD | Modular / Multi-person projects | Standard layouts (src/, app/, internal/) with cleanly decoupled configuration scopes. |

---

## Core Design Principles

1. **YAGNI (You Aren't Gonna Need It)**: Do not generate directories, boilerplates, or abstractions unless an active requirement demands them.
2. **Favor Standard Libraries & Native Features**: Avoid importing external libraries and packages if a standard system library or native platform API satisfies the job.
3. **Symmetry & Clutter-Free**: No source code files sit in root (except for Tier 0/1 entry points). Keep nesting depths below 4 levels.
4. **ponytail: Documentation**: Mark any intentional structural or functional simplifications with code comments so other developers (and agents) understand the choice:
   - `// ponytail: simplified router using standard multiplexer to avoid framework boilerplate`
   - `# ponytail: using sqlite inline queries to avoid SQL-Alchemy setup overhead`

---

## Custom MCP Tools

The plugin bundles a custom Model Context Protocol (MCP) server that exposes high-level workspace-cleaning tools directly to your AI agents:

- **`flatten_directory`**: Moves all files in a single-child nested directory up and deletes the empty parent folder.
- **`prune_empty_folders`**: Recursively deletes all empty directories in the workspace (skipping .git folders).

To enable this server, configure it in your `mcp_config.json` (see Installation section below).

---

## Git Pre-Commit Hook

To prevent cluttered code layouts from being committed, you can install the layout-checking pre-commit hook:

1. **Check Description**: It automatically evaluates staged files before a commit is completed. If any source code files sit in root or nesting depth exceeds 3 levels, it blocks the commit.
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
│   └── neat_freak_mcp.py     # Zero-dependency Python MCP server script
├── scripts/
│   ├── pre_commit_check.py   # Pre-commit checker Python script
│   ├── pre-commit.template   # Shell hook template
│   └── install-hook.sh       # Hook installer bash script
└── skills/
    ├── neat-freak/           # Main Scaffolding Skill
    │   ├── SKILL.md
    │   └── references/       # Stack Blueprints (Go, Python, Rust, TS)
    ├── neat-freak-audit/     # Cleanliness Audit Skill
    │   └── SKILL.md
    ├── neat-freak-review/    # Pull Request / Diff Review Skill
    │   └── SKILL.md
    ├── neat-freak-comfy/     # AI Optimization Skill
    │   └── SKILL.md
    ├── neat-freak-debt/      # Technical Layout Debt Skill
    │   └── SKILL.md
    ├── neat-freak-inspect/   # Dependency Inspector Skill
    │   └── SKILL.md
    └── neat-freak-help/      # Quick Reference Cheatsheet
        └── SKILL.md
```

## Intensity Modes

You can dynamically toggle the plugin's intensity levels or configure default modes:

- **`neat-freak off`**: Completely deactivates all layout checking.
- **`neat-freak on`** (Default): Enforces standard layout guidelines (Tiers 0 and 1).
- **`neat-freak ocd`**: Enforces strict modular layout symmetry (Tier 2 / Full OCD).

### Configuration Priority
1. **Environment Variable**: `NEAT_FREAK_DEFAULT_MODE` (values: `off`, `on`, `ocd`).
2. **Local Configuration File**: `.neat-freak-config.json` placed in the root of your project directory containing `{"defaultMode": "on"}`.
3. **Global Configuration File**: `~/.config/neat-freak/config.json` containing `{"defaultMode": "on"}`.

---

## Installation & Setup

### For Gemini / Antigravity Agents (Global Plugin)
Copy the `neat-freak` plugin directory to the Gemini global plugins path:
```bash
cp -R neat-freak ~/.gemini/config/plugins/
```

### For Claude Code / Claude Agents (Global Skills)
Since Claude loads individual skill packages directly from its global directory, copy the contents of the `skills/` directory:
```bash
cp -R neat-freak/skills/* ~/.claude/skills/
```
To enable the MCP server in Claude Desktop, add the following to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "neat-freak-mcp": {
      "command": "python3",
      "args": ["/Users/siemenvangemert/.claude/skills/neat-freak-comfy/.../neat_freak_mcp.py"]
    }
  }
}
```
