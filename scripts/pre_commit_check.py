#!/usr/bin/env python3
"""
Pre-commit & Layout Review Checker for neat-freak.
Zero external dependencies. Compatible with Python 3.8+.
Evaluates file placement and nesting depth with cross-platform normalization.
"""

import sys
import os
import json
import subprocess

def get_git_files(staged_only=True, working_tree=False):
    try:
        if working_tree:
            cmd = ["git", "status", "--porcelain"]
            output = subprocess.check_output(cmd, text=True)
            files = []
            for line in output.splitlines():
                if len(line) > 3:
                    path = line[3:].strip().split(" -> ")[-1].strip('"')
                    if path:
                        files.append(path)
            return files
        elif staged_only:
            output = subprocess.check_output(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                text=True
            )
            return [line.strip() for line in output.splitlines() if line.strip()]
        else:
            output = subprocess.check_output(
                ["git", "ls-files"],
                text=True
            )
            return [line.strip() for line in output.splitlines() if line.strip()]
    except Exception:
        return []

def resolve_mode(root_path=None):
    env_mode = os.environ.get("NEAT_FREAK_DEFAULT_MODE")
    if env_mode:
        return env_mode.lower()

    if root_path is None:
        try:
            root_path = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                text=True
            ).strip()
        except Exception:
            root_path = os.getcwd()

    local_config = os.path.join(root_path, ".neat-freak-config.json")
    if os.path.exists(local_config):
        try:
            with open(local_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                val = data.get("defaultMode")
                if val:
                    return val.lower()
        except Exception:
            pass

    home = os.path.expanduser("~")
    global_config = os.path.join(home, ".config", "neat-freak", "config.json")
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            global_config = os.path.join(appdata, "neat-freak", "config.json")

    if os.path.exists(global_config):
        try:
            with open(global_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                val = data.get("defaultMode")
                if val:
                    return val.lower()
        except Exception:
            pass

    return "on"

def check_files(files, mode="on"):
    source_exts = {".py", ".ts", ".js", ".go", ".rs", ".java", ".c", ".cpp", ".jsx", ".tsx"}
    skip_dirs = {"node_modules", "target", ".venv", "dist", "build", ".next", ".git", "scratch"}
    max_depth = 3 if mode == "ocd" else 4

    results = []
    for f in files:
        norm_f = f.replace("\\", "/").strip()
        parts = [p for p in norm_f.split("/") if p]
        if not parts:
            continue

        if any(d in parts for d in skip_dirs):
            continue

        filename = parts[-1]
        dir_parts = parts[:-1]
        _, ext = os.path.splitext(filename)

        status = "PASS"
        reason = "Correctly placed."

        if not dir_parts:
            # Sits in root
            if ext.lower() in source_exts:
                status = "FAIL"
                reason = "Stray source file in root directory. Move into application folder (e.g. src/, app/)."
        else:
            if len(dir_parts) > max_depth:
                status = "FAIL"
                reason = f"Excessive nesting depth ({len(dir_parts)} levels, max allowed is {max_depth})."

        results.append({
            "file": norm_f,
            "status": status,
            "reason": reason
        })
    return results

def main():
    args = sys.argv[1:]
    mode = resolve_mode()

    if mode == "off":
        sys.stdout.write("neat-freak: disabled. Skipping layout checks.\n")
        sys.exit(0)

    as_table = "--table" in args or "-t" in args
    working_tree = "--working-tree" in args or "--all" in args
    explicit_files = [a for a in args if not a.startswith("-")]

    if explicit_files:
        files = explicit_files
    else:
        files = get_git_files(staged_only=not working_tree, working_tree=working_tree)

    results = check_files(files, mode)
    violations = [r for r in results if r["status"] == "FAIL"]

    if as_table:
        sys.stdout.write(f"### Neat Freak Placement Review (Mode: {mode.upper()})\n\n")
        if not results:
            sys.stdout.write("No modified files detected to review.\n")
            sys.exit(0)
        sys.stdout.write("| File Path | Status | Finding / Recommendation |\n")
        sys.stdout.write("|---|---|---|\n")
        for r in results:
            sys.stdout.write(f"| `{r['file']}` | **{r['status']}** | {r['reason']} |\n")
        sys.stdout.write("\n")
        sys.exit(1 if violations else 0)

    if violations:
        sys.stderr.write(f"NEAT-FREAK LAYOUT VIOLATIONS DETECTED (Mode: {mode.upper()}):\n")
        for v in violations:
            sys.stderr.write(f"  - [{v['file']}]: {v['reason']}\n")
        sys.stderr.write("\nPlease reorganize your files before committing.\n")
        sys.exit(1)

    sys.stdout.write(f"neat-freak: All {len(results)} evaluated file(s) conform to layout standards (Mode: {mode.upper()}).\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
