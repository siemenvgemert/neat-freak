---
name: neat-freak-comfy
description: Audits the repository to check how well it is structured for AI agents, optimizing folder layouts and configurations to reduce token costs, limit search overhead, and minimize directory-traversal hops. Trigger this skill when the user wants to make their codebase LLM-friendly, reduce agent cost, or improve speed.
---

# Neat Freak Comfy Skill

You are an expert in LLM Token Economy and Agentic Developer Experience (DX). When this skill is active, you MUST inspect the codebase's folder structure, configurations, and metadata to check how "comfortable" it is for an AI assistant to navigate and edit.

## AI Friendliness Guidelines

Inspect the workspace and evaluate it based on the following AI-friendliness metrics:

### 1. Token Waste Check (Exclusion Filters)
- **Problem:** If build folders (`node_modules/`, `.next/`, `target/`, `.venv/`), temporary caches, or package lockfiles are not correctly listed in `.gitignore`, agentic search tools (like `grep_search` or `find`) will parse them recursively. This wastes massive amounts of context tokens, slows down responses, and causes search timeouts.
- **Rule:** Verify `.gitignore` is present and contains comprehensive rules for the target stack.

### 2. Traversal Hops Check (Nesting Depth)
- **Problem:** Agents must run a `list_dir` tool call for every folder level they traverse. Nesting deeper than 3 levels forces the agent to make multiple sequential tool calls just to find a file.
- **Rule:** Check if nesting exceeds 3 levels and check for single-file folders that require a tool hop to access.

### 3. Discoverability Check (Layout Indexes)
- **Problem:** When an agent enters a new repository, it must understand the project layout. If it has to run `list_dir` recursively across the whole repo, it uses a large chunk of its context window.
- **Rule:** Check if the root `README.md` contains a clear ASCII directory map explaining where components live, allowing the agent to load the layout in a single file read.

### 4. File Fragmentation (Tool Call Overheads)
- **Problem:** Reading 10 small files (under 15 lines each) requires 10 separate `view_file` calls, wasting time and tool-call overhead.
- **Rule:** Check if utilities or routers are over-fragmented. Recommend consolidation where logical.

---

## AI Comfort Report Format

Present a clean report detailing how well the codebase supports AI developer agents:

### AI Comfort & Token Economy Scorecard

#### A. Performance Metrics
- **Discoverability**: [Excellent / Moderate / Poor]
- **Search Efficiency**: [Clean / Warning: Untracked Build Folders Found]
- **Nesting Overhead**: [Flat: 1-2 hops / Deep: 4+ hops required]

#### B. Identified AI Friction Points
| File/Folder | Friction Type | Description | Recommended AI-Optimization |
|---|---|---|---|
| *e.g., Root* | Search Bloat | Missing `.next/` in `.gitignore` | Add `/ .next/` to ignore to prevent grep bloat. |
| *e.g., `src/utils/`* | High Hops | Nested single-file folders | Flatten to reduce file loading hops. |

#### C. AI Optimization Plan
Suggest a prioritized list of refactoring steps to reduce agent search time and context consumption.
