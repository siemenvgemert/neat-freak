#!/usr/bin/env python3
"""
Fast Workspace Cleanliness Auditor for neat-freak.
Zero external dependencies. Compatible with Python 3.8+.
Uses os.scandir for high-speed filesystem traversal.
"""

import sys
import os
import json

SKIP_DIRS = {
    ".git", "node_modules", "target", ".venv", "venv", "dist", "build",
    ".next", ".nuxt", "scratch", "__pycache__", ".pytest_cache", ".turbo",
    ".mypy_cache", ".ruff_cache", ".idea", ".vscode", "coverage"
}

SOURCE_EXTENSIONS = {
    ".py", ".ts", ".js", ".go", ".rs", ".java", ".c", ".cpp",
    ".h", ".hpp", ".cs", ".php", ".rb", ".swift", ".kt", ".jsx", ".tsx"
}

def resolve_mode(root_path):
    env_mode = os.environ.get("NEAT_FREAK_DEFAULT_MODE")
    if env_mode:
        return env_mode.lower()

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

def check_gitignore_rules(root_path):
    gitignore_path = os.path.join(root_path, ".gitignore")
    patterns = set()
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.add(line.strip("/"))
        except Exception:
            pass
    return patterns

def scan_workspace(root_path, mode="on"):
    max_nesting = 3 if mode == "ocd" else 4
    gitignore_patterns = check_gitignore_rules(root_path)

    empty_dirs = []
    single_child_dirs = []
    excessive_nesting_files = []
    stray_root_files = []
    unignored_artifacts = []
    duplicate_configs = []

    config_names = {"tsconfig.json", "package.json", ".eslintrc", ".eslintrc.json", ".prettierrc"}
    found_configs = {name: [] for name in config_names}

    # Fast iterative traversal using os.scandir
    def visit_dir(dir_path, rel_path=""):
        try:
            entries = list(os.scandir(dir_path))
        except (PermissionError, FileNotFoundError):
            return

        valid_entries = []
        for e in entries:
            name = e.name
            if name == ".DS_Store":
                continue
            if e.is_dir(follow_symlinks=False) and name in SKIP_DIRS:
                if name in {"node_modules", "target", ".venv", "dist", ".next", "__pycache__"}:
                    if name not in gitignore_patterns:
                        unignored_artifacts.append(os.path.join(rel_path, name).replace("\\", "/"))
                continue
            valid_entries.append(e)

        # 1. Empty Directory Check
        if not valid_entries:
            if rel_path:
                empty_dirs.append(rel_path.replace("\\", "/"))
            return

        # 2. Single-item directory (contains only one subdirectory and no files)
        dir_children = [e for e in valid_entries if e.is_dir(follow_symlinks=False)]
        file_children = [e for e in valid_entries if e.is_file(follow_symlinks=False)]
        if len(dir_children) == 1 and len(file_children) == 0:
            single_child_dirs.append(rel_path.replace("\\", "/"))

        # Process entries
        for e in valid_entries:
            name = e.name
            child_rel = os.path.join(rel_path, name) if rel_path else name
            norm_rel = child_rel.replace("\\", "/")

            if e.is_dir(follow_symlinks=False):
                visit_dir(e.path, child_rel)
            elif e.is_file(follow_symlinks=False):
                if name in config_names and rel_path:
                    found_configs[name].append(norm_rel)

                if not rel_path:
                    _, ext = os.path.splitext(name)
                    if ext in SOURCE_EXTENSIONS:
                        stray_root_files.append(norm_rel)
                else:
                    depth = len([p for p in norm_rel.split("/")[:-1] if p])
                    if depth > max_nesting:
                        excessive_nesting_files.append((norm_rel, depth))

    visit_dir(root_path)

    for cfg_name, occurrences in found_configs.items():
        if len(occurrences) > 1:
            duplicate_configs.extend(occurrences)

    # Calculate Cleanliness Score
    score = 100
    score -= len(stray_root_files) * 10
    score -= len(excessive_nesting_files) * 5
    score -= len(unignored_artifacts) * 8
    score -= len(empty_dirs) * 3
    score -= len(single_child_dirs) * 2
    score -= len(duplicate_configs) * 4
    score = max(0, min(100, score))

    if score >= 90:
        rating = "Immaculate"
    elif score >= 70:
        rating = "Neat but Expandable"
    else:
        rating = "Cluttered"

    violations = []
    for f in stray_root_files:
        violations.append({
            "type": "Stray Root File",
            "path": f,
            "desc": "Source code sits directly in root directory",
            "action": "Move into an application directory (e.g. src/, app/)"
        })
    for f, d in excessive_nesting_files:
        violations.append({
            "type": "Excessive Nesting",
            "path": f,
            "desc": f"Nesting depth of {d} levels exceeds maximum ({max_nesting})",
            "action": "Flatten directory hierarchy"
        })
    for d in empty_dirs:
        violations.append({
            "type": "Empty Directory",
            "path": d,
            "desc": "Directory contains no files",
            "action": "Remove folder using prune_empty_folders"
        })
    for d in single_child_dirs:
        violations.append({
            "type": "Single-Item Folder",
            "path": d,
            "desc": "Directory only contains a single nested folder",
            "action": "Flatten into parent folder"
        })
    for a in unignored_artifacts:
        violations.append({
            "type": "Unignored Artifact",
            "path": a,
            "desc": f"Build/cache artifact '{a}' missing from .gitignore",
            "action": f"Add {a} to .gitignore"
        })
    for c in duplicate_configs:
        violations.append({
            "type": "Duplicate Config",
            "path": c,
            "desc": "Redundant nested configuration file",
            "action": "Consolidate into root configuration"
        })

    return {
        "score": score,
        "rating": rating,
        "mode": mode,
        "max_nesting": max_nesting,
        "violations": violations,
        "stats": {
            "stray_files": len(stray_root_files),
            "excessive_nesting": len(excessive_nesting_files),
            "empty_dirs": len(empty_dirs),
            "single_child_dirs": len(single_child_dirs),
            "unignored_artifacts": len(unignored_artifacts),
            "duplicate_configs": len(duplicate_configs)
        }
    }

def format_markdown(result):
    lines = []
    lines.append(f"### Cleanliness Scorecard: **{result['score']}/100** ({result['rating']})")
    lines.append(f"*Mode: `{result['mode'].upper()}` (Max Allowed Nesting: {result['max_nesting']} levels)*\n")

    if not result["violations"]:
        lines.append("No layout violations found. Workspace structure is pristine!")
        return "\n".join(lines)

    lines.append("| Issue Type | File/Folder Path | Description | Recommended Action |")
    lines.append("|---|---|---|---|")
    for v in result["violations"]:
        lines.append(f"| {v['type']} | `{v['path']}` | {v['desc']} | {v['action']} |")

    lines.append("\n#### Prioritized Cleanup Action Plan")
    actions = []
    if result["stats"]["stray_files"] > 0:
        actions.append("1. **Relocate stray root files** into dedicated application packages.")
    if result["stats"]["unignored_artifacts"] > 0:
        actions.append("2. **Update `.gitignore`** to exclude build/cache directories.")
    if result["stats"]["empty_dirs"] > 0:
        actions.append("3. **Prune empty folders** using `prune_empty_folders`.")
    if result["stats"]["single_child_dirs"] > 0:
        actions.append("4. **Flatten single-child folders** to decrease traversal hops.")
    if result["stats"]["excessive_nesting"] > 0:
        actions.append("5. **Refactor deeply nested modules** to stay within depth limits.")
    lines.extend(actions)
    return "\n".join(lines)

def main():
    root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.getcwd()
    json_output = "--json" in sys.argv

    mode = resolve_mode(root)
    result = scan_workspace(root, mode)

    if json_output:
        sys.stdout.write(json.dumps(result, indent=2) + "\n")
    else:
        sys.stdout.write(format_markdown(result) + "\n")

if __name__ == "__main__":
    main()
