"""Level 3 -- git notes."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 3
TITLE = "git notes"
CATEGORY = "Internals"

NOTE_TEXT = "reviewed-by: alice"

PROMPT = f"""\
This repo has exactly one commit. Attach a git note to it with the exact
text "{NOTE_TEXT}" -- without amending the commit, and without creating
any new commit on top of it. (Notes live outside the normal commit
history, in their own ref.)
"""

HINTS = [
    "git has a whole subcommand for attaching metadata to a commit without "
    "touching the commit itself: `git notes`.",
    f'Try: git notes add -m "{NOTE_TEXT}" HEAD',
]

CANONICAL = f'git notes add -m "{NOTE_TEXT}" HEAD'


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])
    (sandbox_dir / "feature.py").write_text("def feature():\n    pass\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add feature stub"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    commit_count = run_git(sandbox_dir, ["rev-list", "--count", "HEAD"]).stdout.strip()
    if commit_count != "1":
        return False, (
            f"expected exactly 1 commit on HEAD, found {commit_count} -- "
            "notes shouldn't create new commits."
        )

    result = run_git(sandbox_dir, ["notes", "show", "HEAD"], check=False)
    if result.returncode != 0:
        return False, "no note found on HEAD yet."

    note = result.stdout.strip()
    if note == NOTE_TEXT:
        return True, "The note is attached, and HEAD is still the same single commit."

    return False, f"found a note, but its text is '{note}', not '{NOTE_TEXT}'."
