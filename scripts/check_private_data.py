"""Fail if personal tax data could be committed or pushed.

Run before every commit and push:
    python -I scripts/check_private_data.py

Checks, from the repo root:
1. .gitignore contains the required private-folder entries.
2. git reports sample paths inside each private folder as ignored.
3. No tracked file lives under a private folder.
4. No file under a private folder is staged.
5. No commit reachable from any ref ever contained a private-folder path.

Exit code 0 means safe, 1 means a leak risk was found.
"""
import subprocess
import sys

PRIVATE_DIRS = ["my-tax-docs", "my tax files", "analysis"]
REQUIRED_IGNORE_LINES = ["my-tax-docs/", "my tax files/", "analysis/"]


def git(*args):
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8"
    )
    return result.returncode, result.stdout


def main():
    problems = []

    try:
        with open(".gitignore", encoding="utf-8") as fh:
            lines = {line.strip() for line in fh}
    except OSError:
        lines = set()
        problems.append(".gitignore is missing")
    for entry in REQUIRED_IGNORE_LINES:
        if entry not in lines:
            problems.append(f".gitignore is missing the entry '{entry}'")

    for folder in PRIVATE_DIRS:
        code, _ = git("check-ignore", "-q", f"{folder}/sample.pdf")
        if code != 0:
            problems.append(f"git does not ignore '{folder}/'")

    _, tracked = git("ls-files", "--", *PRIVATE_DIRS)
    if tracked.strip():
        problems.append("tracked files inside private folders:\n" + tracked)

    _, staged = git("diff", "--cached", "--name-only", "--", *PRIVATE_DIRS)
    if staged.strip():
        problems.append("staged files inside private folders:\n" + staged)

    _, history = git("log", "--all", "--name-only", "--format=")
    leaked = sorted(
        {
            path
            for path in history.splitlines()
            if any(path.startswith(folder + "/") for folder in PRIVATE_DIRS)
        }
    )
    if leaked:
        problems.append("private paths found in git history:\n" + "\n".join(leaked))

    if problems:
        print("PRIVATE DATA CHECK FAILED")
        for problem in problems:
            print("-", problem)
        return 1
    print("Private data check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
