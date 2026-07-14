import sys
import os
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

def main():
    files = get_staged_files()
    violations = []
    
    # Root source file extensions to check
    source_exts = {".py", ".ts", ".js", ".go", ".rs", ".java", ".c", ".cpp"}
    
    # Paths containing these directories are skipped (third-party/build folders)
    skip_dirs = {"node_modules", "target", ".venv", "dist", "build", ".next", ".git"}
    
    for f in files:
        parts = f.split(os.sep)
        # Skip files inside ignored directories
        if any(d in parts for d in skip_dirs):
            continue
            
        dir_name = os.path.dirname(f)
        _, ext = os.path.splitext(f)
        
        if not dir_name:  # File sits directly in root
            if ext in source_exts:
                violations.append(f"Stray source file in root: {f}")
        else:
            # Check depth of folder structure (excluding git)
            clean_parts = [p for p in parts[:-1] if p and p != "."]
            if len(clean_parts) > 3:
                violations.append(f"Excessive nesting depth ({len(clean_parts)} levels): {f}")
                
    if violations:
        sys.stderr.write("NEAT-FREAK LAYOUT VIOLATIONS DETECTED:\n")
        for v in violations:
            sys.stderr.write(f"  - {v}\n")
        sys.stderr.write("\nPlease reorganize your files before committing.\n")
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
