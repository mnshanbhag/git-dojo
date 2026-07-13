"""Level 11 -- Merge strategies: -X ours/theirs and octopus merges."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 11
TITLE = "Merge strategies: -X theirs and octopus merge"
CATEGORY = "Branching"

HOTFIX_CONTENT = "value=hotfix\n"

PROMPT = """\
main needs two merges:

1. `hotfix` changed shared_config.txt differently than main did, so
   merging it will conflict. Merge it in, but tell git to automatically
   take hotfix's side of any conflict -- no manual resolving.

2. `b1`, `b2`, and `b3` each add one unrelated file and don't conflict
   with each other or with the hotfix merge. Merge all three into main
   with a single merge command (an octopus merge), not three separate
   merges.
"""

HINTS = [
    "Recursive merge takes a -X option for conflict resolution bias: ours "
    "or theirs, picking which side wins automatically on any conflicting "
    "hunk. Separately, `git merge` isn't limited to two branches -- if "
    "none of the branches conflict with each other, it'll create a "
    "single commit merging all of them at once.",
    "Try: git merge -X theirs hotfix -- then: git merge b1 b2 b3",
]

CANONICAL = "git merge -X theirs hotfix\ngit merge b1 b2 b3"


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "shared_config.txt").write_text("value=main\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Base config"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "hotfix"])
    (sandbox_dir / "shared_config.txt").write_text(HOTFIX_CONTENT)
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Hotfix changes config"])

    run_git(sandbox_dir, ["checkout", "-q", "main"])
    (sandbox_dir / "shared_config.txt").write_text("value=main-updated\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Main also changes config"])

    for name, fname in (("b1", "file1.txt"), ("b2", "file2.txt"), ("b3", "file3.txt")):
        run_git(sandbox_dir, ["checkout", "-q", "-b", name])
        (sandbox_dir / fname).write_text(f"{name}\n")
        run_git(sandbox_dir, ["add", "."])
        run_git(sandbox_dir, ["commit", "-q", "-m", f"Add {fname.split('.')[0]}"])
        run_git(sandbox_dir, ["checkout", "-q", "main"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    config_file = sandbox_dir / "shared_config.txt"
    if not config_file.exists() or config_file.read_text() != HOTFIX_CONTENT:
        return False, "shared_config.txt doesn't match hotfix's version -- the -X theirs merge isn't done (or wasn't biased correctly)."

    for fname in ("file1.txt", "file2.txt", "file3.txt"):
        if not (sandbox_dir / fname).exists():
            return False, f"{fname} is missing -- the octopus merge of b1/b2/b3 isn't complete."

    parents = run_git(sandbox_dir, ["log", "-1", "--format=%P"]).stdout.strip().split()
    if len(parents) < 4:
        return False, (
            f"HEAD has {len(parents)} parent(s); expected at least 4 "
            "(the post-hotfix main plus b1, b2, b3) from a single octopus merge."
        )

    return True, "hotfix merged in with -X theirs, and b1/b2/b3 merged together in one octopus merge."
