#!/usr/bin/env python3
"""
Fast Layout Debt Harvester for neat-freak.
Zero external dependencies. Compatible with Python 3.8+.
Scans for ponytail and neat-freak simplification comments in milliseconds.
"""

import sys
import os
import re

SKIP_DIRS = {
    ".git", "node_modules", "target", ".venv", "venv", "dist", "build",
    ".next", ".nuxt", "scratch", "__pycache__", ".pytest_cache", ".turbo",
    ".mypy_cache", ".ruff_cache", ".idea", ".vscode", "coverage"
}

SOURCE_EXTENSIONS = {
    ".py", ".ts", ".js", ".go", ".rs", ".java", ".c", ".cpp",
    ".h", ".hpp", ".cs", ".php", ".rb", ".swift", ".kt", ".jsx", ".tsx",
    ".html", ".css", ".sql", ".sh"
}

PATTERN = re.compile(
    r'(?://|#|/\*)\s*(?:ponytail|neat-freak)\s*:\s*(.*?)(?:\*/|\n|$)',
    re.IGNORECASE
)

def harvest_debt(root_path):
    records = []

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
                _, ext = os.path.splitext(e.name)
                if ext.lower() in SOURCE_EXTENSIONS:
                    norm_path = os.path.join(rel_path, e.name).replace("\\", "/") if rel_path else e.name
                    scan_file(e.path, norm_path, records)

    def scan_file(file_path, norm_path, records):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_no, line in enumerate(f, start=1):
                    match = PATTERN.search(line)
                    if match:
                        desc = match.group(1).strip()
                        if desc:
                            records.append({
                                "file": norm_path,
                                "line": line_no,
                                "description": desc
                            })
        except Exception:
            pass

    visit_dir(root_path)
    return records

def format_markdown(records):
    lines = [
        "# Layout Debt Ledger",
        "",
        "This file tracks all intentional architecture and implementation simplifications in the codebase.",
        ""
    ]
    if not records:
        lines.append("## Staged Simplifications")
        lines.append("")
        lines.append("*No layout debt comments found. Codebase has zero recorded layout simplification debt.*")
    else:
        lines.append("## Staged Simplifications")
        lines.append("")
        lines.append("| File Path | Line | Description |")
        lines.append("|---|---|---|")
        for r in records:
            lines.append(f"| `{r['file']}` | {r['line']} | {r['description']} |")
    return "\n".join(lines)

def main():
    root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.getcwd()
    write_file = "--write" in sys.argv or "-w" in sys.argv

    records = harvest_debt(root)
    content = format_markdown(records)

    if write_file:
        out_path = os.path.join(root, "layout_debt.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        sys.stdout.write(f"Updated layout debt ledger at: {out_path} ({len(records)} entries found)\n")
    else:
        sys.stdout.write(content + "\n")

if __name__ == "__main__":
    main()
