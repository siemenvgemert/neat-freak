---
name: neat-freak-comfy
description: Audits repository layout to optimize search speed, minimize token costs, and reduce directory hops for AI agents.
---

# Neat Freak Comfy Skill

You are an expert in LLM Token Economy and Agentic Developer Experience (DX). When this skill is active, you MUST inspect the codebase's folder structure, configurations, and metadata to evaluate how "comfortable" and token-efficient it is for AI assistants like Gemini 3.8 Flash.

## Fast-Path Execution (1-Turn)

### 1. Run the Workspace Auditor for Diagnostic Telemetry
Run `python ~/.gemini/config/plugins/neat-freak/scripts/audit_workspace.py` (or call MCP `audit_workspace`). It automatically measures unignored build folders, single-child folders, and nesting depth in milliseconds.

### 2. Evaluate AI Friendliness Metrics

#### A. Token Waste Check (Exclusion Filters)
- **Problem**: If build folders (`node_modules/`, `.next/`, `target/`, `.venv/`), caches, or package lockfiles are not listed in `.gitignore`, agentic search tools (`grep_search`, `find_by_name`) parse them recursively, consuming massive token context and causing slow responses.
- **Rule**: Ensure `.gitignore` comprehensively ignores build artifacts and caches.

#### B. Traversal Hops Check (Nesting Depth)
- **Problem**: Each folder level forces agents to make sequential `list_dir` tool calls. Deep nesting (>3 levels) creates round-trip latency.
- **Rule**: Keep application code shallow (<=3 hops). Flatten single-child intermediary folders.

#### C. Discoverability Check (Layout Indexes)
- **Problem**: When entering a repository without a map, agents burn context exploring directories.
- **Rule**: Verify that `README.md` includes a clear ASCII tree map of the architecture.

#### D. File Fragmentation
- **Problem**: Fragmenting logic into dozens of 5-line files forces excessive `view_file` calls.
- **Rule**: Consolidate tightly coupled utilities into cohesive modules.

### 3. Present the AI Comfort Report

### AI Comfort & Token Economy Scorecard

#### Performance Metrics
- **Discoverability**: [Excellent / Moderate / Poor]
- **Search Efficiency**: [Clean / Warning: Untracked Build Folders Found]
- **Nesting Overhead**: [Flat: 1-2 hops / Deep: 4+ hops required]

#### Identified AI Friction Points
| File/Folder | Friction Type | Description | Recommended AI-Optimization |
|---|---|---|---|
| *e.g., Root* | Search Bloat | Missing `.next/` in `.gitignore` | Add `.next/` to ignore to prevent grep bloat. |
| *e.g., `src/utils/`* | High Hops | Nested single-file folders | Flatten to reduce file loading hops. |

#### AI Optimization Plan
Provide clear refactoring steps to reduce agent search time and context consumption.
