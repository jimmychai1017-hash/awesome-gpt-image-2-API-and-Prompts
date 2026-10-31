#!/usr/bin/env python3
"""PreToolUse hook: run the repository checks before any `git commit`.

Claude Code passes the pending tool call as JSON on stdin. Commands that are
not a git commit pass straight through. For a commit, a failing check exits 2,
which blocks the call and shows stderr to Claude so it fixes the problem first.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
COMMIT_RE = re.compile(r"(^|[;&|(]|\s)git(\s+-[cC]\s+\S+)*\s+commit\b")

CHECKS = [
    ["python3", "scripts/verify_prompt_repo.py"],
    ["python3", "-m", "json.tool", "data/ingested_tweets.json"],
    ["python3", ".claude/skills/sync-localized-readmes/check_locale_parity.py"],
    ["git", "diff", "--cached", "--check"],
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not COMMIT_RE.search(command):
        return 0

    failures = []
    for check in CHECKS:
        result = subprocess.run(check, cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip().splitlines()
            failures.append(f"$ {' '.join(check)}  (exit {result.returncode})\n" + "\n".join(output[-25:]))

    if failures:
        print("Commit blocked: repository checks failed (see CLAUDE.md, 铁律 12).\n", file=sys.stderr)
        print("\n\n".join(failures), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
