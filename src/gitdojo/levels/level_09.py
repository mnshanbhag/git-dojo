"""Level 9 -- rerere: recorded conflict resolution."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 9
TITLE = "rerere: recorded conflict resolution"
CATEGORY = "History"

PROMPT = """\
main and feature-a both changed config.txt's one line differently, so
merging feature-a into main conflicts.

1. Enable rerere, then merge feature-a into main. Resolve the conflict by
   keeping main's value ("key=value_from_main"), then complete the merge.
2. Undo *just* the merge (not the branches), then redo the exact same
   merge -- rerere should replay your recorded resolution automatically,
   without you touching the file this time.

End state: main has feature-a merged in via a real merge commit,
config.txt contains exactly "key=value_from_main" with no conflict
markers, and there's a recorded resolution under .git/rr-cache.
"""

HINTS = [
    "rerere ('reuse recorded resolution') isn't on by default -- you have "
    "to opt in with a config setting before it starts remembering how you "
    "resolved a conflict.",
    "Try: git config rerere.enabled true; git merge feature-a; resolve "
    "config.txt to 'key=value_from_main'; git add config.txt && git "
    "commit --no-edit; then git reset --hard HEAD^ (undoes just the "
    "merge); git merge feature-a again -- it should resolve itself; "
    "git add config.txt && git commit --no-edit.",
]

CANONICAL = (
    "git config rerere.enabled true\n"
    "git merge feature-a                     # conflicts on config.txt\n"
    '# resolve: set config.txt to "key=value_from_main"\n'
    "git add config.txt && git commit --no-edit\n"
    "git reset --hard HEAD^                  # undo just the merge\n"
    "git merge feature-a                     # rerere replays the resolution\n"
    "git add config.txt && git commit --no-edit"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "config.txt").write_text("key=old_value\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Base config"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "feature-a"])
    (sandbox_dir / "config.txt").write_text("key=value_from_a\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Feature A changes config"])

    run_git(sandbox_dir, ["checkout", "-q", "main"])
    (sandbox_dir / "config.txt").write_text("key=value_from_main\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Main changes config"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    rr_cache = sandbox_dir / ".git" / "rr-cache"
    if not rr_cache.exists() or not any(rr_cache.iterdir()):
        return False, (
            "no recorded rerere resolution found -- make sure "
            "rerere.enabled was set to true before you resolved the "
            "conflict the first time."
        )

    config_file = sandbox_dir / "config.txt"
    if not config_file.exists():
        return False, "config.txt is missing."
    content = config_file.read_text()
    if content != "key=value_from_main\n":
        return False, f"config.txt contains {content!r}, expected 'key=value_from_main\\n' with no conflict markers."

    merges = run_git(
        sandbox_dir, ["log", "--merges", "--format=%H", "main"]
    ).stdout.strip().splitlines()
    if not merges:
        return False, "no merge commit found on main -- did you complete the merge with a commit?"

    return True, "feature-a is merged into main, resolved correctly, and rerere has a recorded resolution."
