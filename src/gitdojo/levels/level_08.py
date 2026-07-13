"""Level 8 -- Reflog recovery."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 8
TITLE = "Reflog recovery"
CATEGORY = "History"

PROMPT = """\
Someone just ran `git reset --hard HEAD~1` on main -- the "Critical bug
fix" commit is no longer reachable from any branch or tag. Nothing is
actually deleted yet: git keeps a log of everywhere HEAD has pointed.

Use the reflog to find that commit, and get `main` pointing at it again.
"""

HINTS = [
    "`git reflog` shows every position HEAD has been at, including the "
    "one you just reset away from.",
    "Run `git reflog`, find the entry for 'Critical bug fix' (it's the "
    "one right before the 'reset: moving to HEAD~1' line), then run "
    "`git reset --hard <that-sha>`.",
]

CANONICAL = (
    "git reflog                 # find the sha for 'Critical bug fix'\n"
    "git reset --hard <that-sha>"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "notes.txt").write_text("v1\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Initial notes"])

    (sandbox_dir / "notes.txt").write_text("v1\nv2\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Update notes"])

    (sandbox_dir / "critical_fix.py").write_text("important = True\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Critical bug fix"])

    run_git(sandbox_dir, ["reset", "-q", "--hard", "HEAD~1"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    reflog = run_git(
        sandbox_dir, ["reflog", "--format=%H %gs"]
    ).stdout.strip().splitlines()
    lost_matches = [
        line.split(maxsplit=1)[0]
        for line in reflog
        if line.split(maxsplit=1)[1:2] == ["commit: Critical bug fix"]
    ]
    if not lost_matches:
        return False, (
            "couldn't find the lost commit in the reflog -- don't run "
            "`git reflog expire` or `git gc` here."
        )
    lost_sha = lost_matches[0]

    current = run_git(sandbox_dir, ["rev-parse", "main"]).stdout.strip()
    if current == lost_sha:
        return True, "main is back at the lost 'Critical bug fix' commit."

    return False, f"main is at {current}, not the lost commit ({lost_sha})."
