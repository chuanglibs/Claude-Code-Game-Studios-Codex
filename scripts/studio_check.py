#!/usr/bin/env python3
"""Run a shared Claude validator explicitly, without committing or pushing.

Requires Git and Bash (Git Bash on Windows). Preserves the hook's exit code.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("commit", "push"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Project root (defaults to the script's repository)")
    args = parser.parse_args()
    root = args.root.resolve()
    hook = Path(".claude/hooks") / f"validate-{args.kind}.sh"
    if not (root / hook).is_file():
        print(f"Missing hook: {hook}", file=sys.stderr)
        return 2
    bash = shutil.which("bash")
    if not bash or not shutil.which("git"):
        print("Git and Bash are required. On Windows, use Git Bash.", file=sys.stderr)
        return 2
    if subprocess.run(["git", "rev-parse", "--git-dir"], cwd=root,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        print(f"Not a Git repository: {root}", file=sys.stderr)
        return 2
    payload = {"tool_name": "Bash", "tool_input": {"command": f"git {args.kind}"}}
    print(f"Running {hook.as_posix()} (validation only; no {args.kind}).", flush=True)
    try:
        return subprocess.run(
            [bash, hook.as_posix()], cwd=root, input=json.dumps(payload),
            text=True, timeout=30,
        ).returncode
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"Studio check failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
