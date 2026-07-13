"""Level 5 -- rebase --onto."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 5
TITLE = "rebase --onto: reparenting a branch"
CATEGORY = "History"

PROMPT = """\
`feature` was accidentally branched off `staging` instead of `main`, so
it carries staging's "Staging-only tweak" commit in its history -- a
commit that must never end up in feature or in main.

Reparent `feature` so it sits directly on top of `main`, keeping only its
own two commits ("Feature part 1", "Feature part 2"), with staging's
commit gone from its history entirely. Do it with a single rebase
command -- don't cherry-pick the commits by hand.
"""

HINTS = [
    "There's a rebase mode built exactly for 'take these commits and replay "
    "them onto a different base, dropping what's currently underneath "
    "them'. It takes three arguments: the new base, the old base (whose "
    "commits should be dropped), and the branch to move.",
    "Try: git rebase --onto main staging feature",
]

CANONICAL = "git rebase --onto main staging feature"


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])
    (sandbox_dir / "file.txt").write_text("base\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Base"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "staging"])
    (sandbox_dir / "file.txt").write_text("base\nstaging-only\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Staging-only tweak"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "feature"])
    (sandbox_dir / "feature.txt").write_text("f1\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Feature part 1"])
    (sandbox_dir / "feature.txt").write_text("f1\nf2\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Feature part 2"])

    run_git(sandbox_dir, ["checkout", "-q", "main"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    branches = run_git(
        sandbox_dir, ["branch", "--format=%(refname:short)"]
    ).stdout.split()
    for name in ("main", "staging", "feature"):
        if name not in branches:
            return False, f"branch '{name}' is missing."

    on_main = run_git(
        sandbox_dir, ["merge-base", "--is-ancestor", "main", "feature"], check=False
    )
    if on_main.returncode != 0:
        return False, "main is not an ancestor of feature -- feature isn't based on main."

    on_staging = run_git(
        sandbox_dir, ["merge-base", "--is-ancestor", "staging", "feature"], check=False
    )
    if on_staging.returncode == 0:
        return False, "staging is still an ancestor of feature -- its commit is still there."

    count = run_git(sandbox_dir, ["rev-list", "--count", "main..feature"]).stdout.strip()
    if count != "2":
        return False, f"expected exactly 2 commits on feature past main, found {count}."

    messages = run_git(
        sandbox_dir, ["log", "--format=%s", "main..feature"]
    ).stdout.strip().splitlines()
    if set(messages) != {"Feature part 1", "Feature part 2"}:
        return False, f"unexpected commit messages on feature: {messages}"

    return True, "feature now sits directly on main, with staging's commit gone from its history."
