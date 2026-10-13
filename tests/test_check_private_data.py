"""Tests for scripts/check_private_data.py using throwaway git repos."""
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts",
    "check_private_data.py",
)
GOOD_IGNORE = "my-tax-docs/\nmy tax files/\nanalysis/\n"


def git(cwd, *args):
    subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    )


def make_repo(root, ignore=GOOD_IGNORE):
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")
    with open(os.path.join(root, ".gitignore"), "w", encoding="utf-8") as fh:
        fh.write(ignore)
    git(root, "add", ".gitignore")
    git(root, "commit", "-q", "-m", "init")


def run_check(root):
    return subprocess.run(
        [sys.executable, "-I", SCRIPT], cwd=root, capture_output=True, text=True
    )


class CheckPrivateDataTest(unittest.TestCase):
    def test_passes_on_clean_repo(self):
        with tempfile.TemporaryDirectory() as root:
            make_repo(root)
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("Private data check passed.", result.stdout)

    def test_fails_when_ignore_entry_missing(self):
        with tempfile.TemporaryDirectory() as root:
            make_repo(root, ignore="my-tax-docs/\nmy tax files/\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("analysis/", result.stdout)

    def test_fails_when_private_path_force_added(self):
        with tempfile.TemporaryDirectory() as root:
            make_repo(root)
            os.makedirs(os.path.join(root, "analysis"))
            with open(os.path.join(root, "analysis", "x.txt"), "w") as fh:
                fh.write("synthetic")
            git(root, "add", "-f", "analysis/x.txt")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("analysis/x.txt", result.stdout)


if __name__ == "__main__":
    unittest.main()
