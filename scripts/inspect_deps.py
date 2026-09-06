#!/usr/bin/env python3
"""
Fast Dependency & Architecture Inspector for neat-freak.
Zero external dependencies. Compatible with Python 3.8+.
Uses AST (Python) and regex scanners to detect circular dependencies and layer violations in milliseconds.
"""

import sys
import os
import ast
import re

SKIP_DIRS = {
    ".git", "node_modules", "target", ".venv", "venv", "dist", "build",
    ".next", ".nuxt", "scratch", "__pycache__", ".pytest_cache", ".turbo",
    ".mypy_cache", ".ruff_cache", ".idea", ".vscode", "coverage"
}

LAYER_PRESENTATION = {"api", "routes", "routers", "controllers", "views", "handlers", "cmd", "cli"}
LAYER_CORE = {"core", "domain", "models", "services", "internal", "entities", "db", "repository"}

TS_IMPORT_RE = re.compile(r'''(?:import\s+.*?from\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\))''')
GO_IMPORT_RE = re.compile(r'''import\s+(?:\(\s*([^)]+)\s*\)|"([^"]+)")''', re.DOTALL)
RUST_USE_RE = re.compile(r'''(?:use|mod)\s+([^;]+);''')

def find_source_files(root_path):
    files_by_type = {"py": {}, "js_ts": {}, "go": {}, "rust": {}}

    def visit_dir(dir_path, rel_path=""):
        try:
            entries = list(os.scandir(dir_path))
        except (PermissionError, FileNotFoundError):
            return

        for e in entries:
            if e.is_dir(follow_symlinks=False):
                if e.name not in SKIP_DIRS and not e.name.startswith("."):
                    visit_dir(e.path, os.path.join(rel_path, e.name) if rel_path else e.name)
            elif e.is_file(follow_symlinks=False):
                norm_rel = os.path.join(rel_path, e.name).replace("\\", "/") if rel_path else e.name
                _, ext = os.path.splitext(e.name)
                ext = ext.lower()
                if ext == ".py":
                    files_by_type["py"][norm_rel] = e.path
                elif ext in {".ts", ".tsx", ".js", ".jsx", ".mjs"}:
                    files_by_type["js_ts"][norm_rel] = e.path
                elif ext == ".go":
                    files_by_type["go"][norm_rel] = e.path
                elif ext == ".rs":
                    files_by_type["rust"][norm_rel] = e.path

    visit_dir(root_path)
    return files_by_type

def parse_python_imports(file_path, rel_path, all_py_files):
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                level = node.level
                # Handle relative imports
                if level > 0:
                    parts = rel_path.split("/")[:-1]
                    if level <= len(parts):
                        base_parts = parts[:len(parts) - level + 1]
                        target = "/".join(base_parts) + ("/" + mod.replace(".", "/") if mod else "")
                        imports.add(target.strip("/"))
                else:
                    imports.add(mod)
    except Exception:
        pass

    # Resolve to actual workspace files
    resolved = set()
    for imp in imports:
        imp_path = imp.replace(".", "/")
        for candidate in all_py_files:
            cand_no_ext, _ = os.path.splitext(candidate)
            if cand_no_ext == imp_path or cand_no_ext.endswith("/" + imp_path) or candidate == imp_path + "/__init__.py":
                if candidate != rel_path:
                    resolved.add(candidate)
    return resolved

def parse_jsts_imports(file_path, rel_path, all_jsts_files):
    resolved = set()
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for match in TS_IMPORT_RE.finditer(content):
            target = match.group(1) or match.group(2)
            if target and (target.startswith("./") or target.startswith("../")):
                dir_rel = os.path.dirname(rel_path)
                norm_target = os.path.normpath(os.path.join(dir_rel, target)).replace("\\", "/")
                # Match with known files
                for cand in all_jsts_files:
                    cand_no_ext, _ = os.path.splitext(cand)
                    if cand == norm_target or cand_no_ext == norm_target or cand == norm_target + "/index":
                        if cand != rel_path:
                            resolved.add(cand)
    except Exception:
        pass
    return resolved

def find_cycles(graph):
    cycles = []
    visited = {}
    path = []

    def dfs(node):
        visited[node] = 1 # in progress
        path.append(node)
        for neighbor in graph.get(node, []):
            if visited.get(neighbor) == 1:
                idx = path.index(neighbor)
                cycle = path[idx:] + [neighbor]
                # Canonicalize cycle
                canon = min(cycle[:-1])
                c_idx = cycle.index(canon)
                cycle_norm = tuple(cycle[c_idx:-1] + cycle[:c_idx] + [canon])
                if cycle_norm not in [tuple(c) for c in cycles]:
                    cycles.append(list(cycle_norm))
            elif visited.get(neighbor, 0) == 0:
                dfs(neighbor)
        path.pop()
        visited[node] = 2 # finished

    for n in list(graph.keys()):
        if visited.get(n, 0) == 0:
            dfs(n)

    return cycles

def check_layer_violations(graph):
    violations = []
    for src, targets in graph.items():
        src_parts = set(src.split("/")[:-1])
        src_is_core = bool(src_parts & LAYER_CORE)
        if not src_is_core:
            continue

        for tgt in targets:
            tgt_parts = set(tgt.split("/")[:-1])
            tgt_is_pres = bool(tgt_parts & LAYER_PRESENTATION)
            if tgt_is_pres:
                violations.append({
                    "src": src,
                    "target": tgt,
                    "desc": f"Core business layer '{src}' directly imports presentation layer '{tgt}'."
                })
    return violations

def inspect_dependencies(root_path):
    files_by_type = find_source_files(root_path)
    graph = {}

    # 1. Python imports
    py_files = set(files_by_type["py"].keys())
    for rel_path, abs_path in files_by_type["py"].items():
        graph[rel_path] = list(parse_python_imports(abs_path, rel_path, py_files))

    # 2. TS/JS imports
    jsts_files = set(files_by_type["js_ts"].keys())
    for rel_path, abs_path in files_by_type["js_ts"].items():
        graph[rel_path] = list(parse_jsts_imports(abs_path, rel_path, jsts_files))

    # Cycle detection
    cycles = find_cycles(graph)

    # Layer violations
    layer_violations = check_layer_violations(graph)

    # Scoring
    score = 100
    score -= len(cycles) * 25
    score -= len(layer_violations) * 15
    score = max(0, min(100, score))

    if score >= 90:
        rating = "Decoupled (Immaculate)"
    elif score >= 70:
        rating = "Decoupled but Fragile"
    else:
        rating = "Tightly Coupled"

    return {
        "score": score,
        "rating": rating,
        "cycles": cycles,
        "layer_violations": layer_violations,
        "total_modules_analyzed": len(graph)
    }

def format_markdown(res):
    lines = [
        f"### Dependency Audit Score: **{res['score']}/100** ({res['rating']})",
        f"*Total Modules Analyzed: {res['total_modules_analyzed']}*",
        ""
    ]

    has_issues = bool(res["cycles"] or res["layer_violations"])
    if not has_issues:
        lines.append("Zero circular dependencies or layer boundary violations detected. Modules are cleanly decoupled.")
        return "\n".join(lines)

    lines.append("| Violation Type | Source Path | Target Path | Description | Recommended Refactoring |")
    lines.append("|---|---|---|---|---|")

    for cycle in res["cycles"]:
        chain = " -> ".join([f"`{c}`" for c in cycle])
        lines.append(f"| Circular Dependency | `{cycle[0]}` | `{cycle[1]}` | Cycle chain: {chain} | Introduce shared interface/context module |")

    for lv in res["layer_violations"]:
        lines.append(f"| Layer Violation | `{lv['src']}` | `{lv['target']}` | {lv['desc']} | Invert dependency via abstraction or event |")

    return "\n".join(lines)

def main():
    root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.getcwd()
    res = inspect_dependencies(root)
    sys.stdout.write(format_markdown(res) + "\n")

if __name__ == "__main__":
    main()
