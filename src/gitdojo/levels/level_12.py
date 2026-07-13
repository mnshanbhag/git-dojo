"""Level 12 -- Worktrees."""

from pathlib import Path

from gitdojo.sandbox import remove_dir, run_git

ID = 12
TITLE = "Worktrees"
CATEGORY = "Branching"

WORKTREE_DIRNAME = "hotfix-wt"

PROMPT = f"""\
This sandbox is checked out on `feature` -- leave it there, don't switch
branches here. An urgent hotfix is needed on top of `main`, but you can't
interrupt your feature work by checking main out in this same directory.

Use `git worktree add` to create a second working tree at
`../{WORKTREE_DIRNAME}` (a sibling of this sandbox directory), on a new
branch called `hotfix`, based on `main`. In that new worktree, create
hotfix.txt containing exactly "urgent fix\\n" and commit it.
"""

HINTS = [
    "git worktree add lets you check out another branch into a completely "
    "separate directory, backed by the same repository -- no need to "
    "stash or switch branches in your current directory.",
    f"Try: git worktree add ../{WORKTREE_DIRNAME} -b hotfix main -- then cd "
    "into it, create hotfix.txt, and commit.",
]

CANONICAL = (
    f"git worktree add ../{WORKTREE_DIRNAME} -b hotfix main\n"
    f"cd ../{WORKTREE_DIRNAME}\n"
    'echo "urgent fix" > hotfix.txt\n'
    'git add hotfix.txt && git commit -m "Add urgent hotfix"'
)


def setup(sandbox_dir: Path) -> None:
    remove_dir(sandbox_dir.parent / WORKTREE_DIRNAME)

    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "file.txt").write_text("base\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Base"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "feature"])
    (sandbox_dir / "file.txt").write_text("base\nfeature work\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Feature work"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    worktree_dir = sandbox_dir.parent / WORKTREE_DIRNAME
    if not worktree_dir.exists():
        return False, f"{WORKTREE_DIRNAME} doesn't exist next to the sandbox yet."

    if not (worktree_dir / ".git").is_file():
        return False, (
            f"{WORKTREE_DIRNAME}/.git isn't a linked-worktree file -- use "
            "`git worktree add`, not a separate `git init` or clone."
        )

    current_branch = run_git(sandbox_dir, ["branch", "--show-current"]).stdout.strip()
    if current_branch != "feature":
        return False, f"this sandbox is now on '{current_branch}', not 'feature' -- that's the whole point of worktrees."

    wt_branch = run_git(worktree_dir, ["branch", "--show-current"]).stdout.strip()
    if wt_branch != "hotfix":
        return False, f"{WORKTREE_DIRNAME} is on '{wt_branch}', expected 'hotfix'."

    is_anc = run_git(sandbox_dir, ["merge-base", "--is-ancestor", "main", "hotfix"], check=False)
    if is_anc.returncode != 0:
        return False, "hotfix doesn't look like it's based on main."

    hotfix_file = worktree_dir / "hotfix.txt"
    if not hotfix_file.exists() or hotfix_file.read_text() != "urgent fix\n":
        return False, "hotfix.txt is missing or doesn't contain 'urgent fix' in the new worktree."

    dirty = run_git(worktree_dir, ["status", "--porcelain"]).stdout.strip()
    if dirty:
        return False, "there are uncommitted changes in the hotfix worktree -- commit hotfix.txt."

    return True, "hotfix.txt is committed on hotfix in a separate worktree, and feature here is untouched."
