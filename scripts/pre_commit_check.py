import sys
import os
import json
import subprocess

def get_staged_files():
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            text=True
        )
        return [line.strip() for line in output.splitlines() if line.strip()]
    except Exception:
        return []

def resolve_mode():
    # 1. Environment variable
    env_mode = os.environ.get("NEAT_FREAK_DEFAULT_MODE")
    if env_mode:
        return env_mode.lower()

    # 2. Local config file in root of Git repo
    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True
        ).strip()
        local_config_path = os.path.join(git_root, ".neat-freak-config.json")
        if os.path.exists(local_config_path):
            with open(local_config_path, "r") as f:
                data = json.load(f)
                val = data.get("defaultMode")
                if val:
                    return val.lower()
    except Exception:
        pass

    # 3. Global config file
    home = os.path.expanduser("~")
    global_config_path = os.path.join(home, ".config", "neat-freak", "config.json")
    if os.name == "nt": # Windows
        appdata = os.environ.get("APPDATA")
        if appdata:
            global_config_path = os.path.join(appdata, "neat-freak", "config.json")

    if os.path.exists(global_config_path):
        try:
            with open(global_config_path, "r") as f:
                data = json.load(f)
                val = data.get("defaultMode")
                if val:
                    return val.lower()
        except Exception:
            pass

    return "on" # default fallback

def main():
    mode = resolve_mode()
    if mode == "off":
        sys.stdout.write("neat-freak: disabled. Skipping layout checks.\n")
        sys.exit(0)

    files = get_staged_files()
    violations = []
    
    # Root source file extensions to check
    source_exts = {".py", ".ts", ".js", ".go", ".rs", ".java", ".c", ".cpp"}
    
    # Paths containing these directories are skipped (third-party/build folders)
    skip_dirs = {"node_modules", "target", ".venv", "dist", "build", ".next", ".git", "scratch"}
    
    for f in files:
        parts = f.split(os.sep)
        # Skip files inside ignored directories
        if any(d in parts for d in skip_dirs):
            continue
            
        dir_name = os.path.dirname(f)
        _, ext = os.path.splitext(f)
        
        # Check root files
        if not dir_name:  # File sits directly in root
            if ext in source_exts:
                violations.append(f"Stray source file in root: {f}")
        else:
            # Check depth of folder structure (excluding git)
            clean_parts = [p for p in parts[:-1] if p and p != "."]
            
            # Enforce limits based on mode
            if mode == "ocd":
                # Strict Full OCD checks: max nesting depth is 3
                if len(clean_parts) > 3:
                    violations.append(f"[Full OCD] Excessive nesting depth ({len(clean_parts)} levels): {f}")
            else:
                # Standard 'on' check: max nesting depth is 4
                if len(clean_parts) > 4:
                    violations.append(f"[On] Excessive nesting depth ({len(clean_parts)} levels): {f}")
                
    if violations:
        sys.stderr.write(f"NEAT-FREAK LAYOUT VIOLATIONS DETECTED (Mode: {mode.upper()}):\n")
        for v in violations:
            sys.stderr.write(f"  - {v}\n")
        sys.stderr.write("\nPlease reorganize your files before committing.\n")
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
