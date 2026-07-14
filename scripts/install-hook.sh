#!/bin/bash
# Installer script for the neat-freak Git pre-commit hook

if [ ! -d ".git" ]; then
  echo "Error: This command must be run from the root of a Git repository."
  exit 1
fi

mkdir -p .git/hooks
cp scripts/pre-commit.template .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "neat-freak Git pre-commit hook successfully installed at .git/hooks/pre-commit"
