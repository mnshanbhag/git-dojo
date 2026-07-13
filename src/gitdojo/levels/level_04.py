"""Level 4 -- Interactive rebase: fixup + autosquash."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 4
TITLE = "Interactive rebase: fixup + autosquash"
CATEGORY = "History"

BUGGY = 'def login():\n    return "Ok"\n'
FIXED = 'def login():\n    return "OK"\n'

PROMPT = """\
app.py has a bug: login() returns "Ok" but should return "OK" (all caps).
There's only one commit, "Add login feature", which introduced the bug.

Fix the bug, but don't make a normal commit for it. Instead, commit the
fix as a *fixup* commit targeting the buggy commit, then use interactive
rebase with autosquash to fold it back in automatically. When you're
done there should be exactly one commit, still titled "Add login
feature", with the bug fixed.

(To run autosquash without an editor popping up, set GIT_SEQUENCE_EDITOR
to a no-op, e.g. `true`, before the rebase command.)
"""

HINTS = [
    "There are two pieces here: a commit that's *marked* as a fix for an "
    "earlier commit (git commit --fixup <target>), and a rebase mode that "
    "automatically reorders and squashes those marked commits into their "
    "targets (--autosquash).",
    'Try: fix app.py, `git add .`, `git commit --fixup HEAD`, then '
    "`GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash --root`.",
]

CANONICAL = (
    "git add app.py\n"
    "git commit --fixup HEAD\n"
    "GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash --root"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])
    (sandbox_dir / "app.py").write_text(BUGGY)
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add login feature"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    app_file = sandbox_dir / "app.py"
    if not app_file.exists():
        return False, "app.py is missing."

    content = app_file.read_text()
    if content != FIXED:
        return False, 'app.py does not contain the fixed \'return "OK"\' yet.'

    commit_count = run_git(sandbox_dir, ["rev-list", "--count", "HEAD"]).stdout.strip()
    if commit_count != "1":
        return False, (
            f"expected exactly 1 commit, found {commit_count} -- the fixup "
            "commit needs to be squashed into the original, not left "
            "sitting on top of it."
        )

    subject = run_git(sandbox_dir, ["log", "-1", "--format=%s"]).stdout.strip()
    if subject != "Add login feature":
        return False, f"HEAD's commit message is '{subject}', expected 'Add login feature'."

    return True, "One commit, correct message, bug fixed -- the fixup squashed cleanly."
