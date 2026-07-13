"""Level 6 -- Splitting a commit (rebase edit + reset)."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 6
TITLE = "Splitting a commit"
CATEGORY = "History"

UTILS_CONTENT = "def helper():\n    return 42\n"
CONFIG_CONTENT = "DEBUG = True\n"

PROMPT = """\
The tip commit ("Add utils and config") bundles two unrelated additions:
utils.py and config.py. Split it into two commits, in this order:
1. "Add utils" -- containing only utils.py
2. "Add config" -- containing only config.py

Use interactive rebase to pause on that commit and edit it, rather than
just resetting the branch and starting over.
"""

HINTS = [
    "Interactive rebase can stop on a specific commit for you to edit it. "
    "Once stopped there, a reset flag unstages that commit's changes back "
    "into your working tree without discarding them, so you can commit "
    "them again in pieces.",
    "Try: git rebase -i HEAD~1 (change 'pick' to 'edit', save & close), "
    "then git reset HEAD^, then commit utils.py and config.py separately, "
    "then git rebase --continue.",
]

CANONICAL = (
    "git rebase -i HEAD~1      # change 'pick' to 'edit' for the commit\n"
    "git reset HEAD^\n"
    'git add utils.py && git commit -m "Add utils"\n'
    'git add config.py && git commit -m "Add config"\n'
    "git rebase --continue"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "README.md").write_text("# project\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Initial commit"])

    (sandbox_dir / "utils.py").write_text(UTILS_CONTENT)
    (sandbox_dir / "config.py").write_text(CONFIG_CONTENT)
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add utils and config"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    messages = run_git(
        sandbox_dir, ["log", "--format=%s", "--reverse"]
    ).stdout.strip().splitlines()
    expected_messages = ["Initial commit", "Add utils", "Add config"]
    if messages != expected_messages:
        return False, f"expected commit sequence {expected_messages}, found {messages}"

    shas = run_git(
        sandbox_dir, ["log", "--format=%H", "--reverse"]
    ).stdout.strip().splitlines()

    utils_files = run_git(
        sandbox_dir, ["diff-tree", "--no-commit-id", "--name-only", "-r", shas[1]]
    ).stdout.split()
    if utils_files != ["utils.py"]:
        return False, f"the 'Add utils' commit touches {utils_files}, expected only utils.py"

    config_files = run_git(
        sandbox_dir, ["diff-tree", "--no-commit-id", "--name-only", "-r", shas[2]]
    ).stdout.split()
    if config_files != ["config.py"]:
        return False, f"the 'Add config' commit touches {config_files}, expected only config.py"

    if not (sandbox_dir / "utils.py").exists() or (sandbox_dir / "utils.py").read_text() != UTILS_CONTENT:
        return False, "utils.py's final content doesn't match the original."
    if not (sandbox_dir / "config.py").exists() or (sandbox_dir / "config.py").read_text() != CONFIG_CONTENT:
        return False, "config.py's final content doesn't match the original."

    return True, "The commit is split cleanly: utils.py and config.py each in their own commit."
