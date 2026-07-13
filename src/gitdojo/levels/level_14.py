"""Level 14 -- Advanced stash: partial stash, named stashes, stash-to-branch."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 14
TITLE = "Advanced stash"
CATEGORY = "Branching"

ORIGINAL_A = "original a\n"
ORIGINAL_B = "original b\n"
FIXED_A = "original a\nurgent fix line\n"

PROMPT = """\
file_a.txt and file_b.txt both have uncommitted changes, but they're
unrelated: file_a.txt has an urgent fix, file_b.txt has unfinished work.

1. Stash them SEPARATELY with descriptive messages: the file_a.txt change
   as "urgent-fix", then the file_b.txt change as "wip-feature".
2. Turn the "urgent-fix" stash into a new branch called
   "urgent-fix-branch", with that change applied there, in one command.
3. The "wip-feature" stash should remain in the stash list, untouched.
"""

HINTS = [
    "`git stash push` takes a pathspec, so you can stash changes to just "
    "one file at a time instead of everything at once, each with its own "
    "-m message. Separately, `git stash branch <name> [<stash>]` creates "
    "a new branch from where the stash was made and applies it there, all "
    "in one step.",
    'Try: git stash push -m "urgent-fix" -- file_a.txt ; '
    'git stash push -m "wip-feature" -- file_b.txt ; git stash list '
    "(to find urgent-fix's index) ; git stash branch urgent-fix-branch stash@{n}",
]

CANONICAL = (
    'git stash push -m "urgent-fix" -- file_a.txt\n'
    'git stash push -m "wip-feature" -- file_b.txt\n'
    "git stash list                              # find urgent-fix's index\n"
    "git stash branch urgent-fix-branch stash@{n}"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "file_a.txt").write_text(ORIGINAL_A)
    (sandbox_dir / "file_b.txt").write_text(ORIGINAL_B)
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Base files"])

    (sandbox_dir / "file_a.txt").write_text(FIXED_A)
    (sandbox_dir / "file_b.txt").write_text(ORIGINAL_B + "wip change line\n")


def check(sandbox_dir: Path) -> tuple[bool, str]:
    current_branch = run_git(sandbox_dir, ["branch", "--show-current"]).stdout.strip()
    if current_branch != "urgent-fix-branch":
        return False, f"current branch is '{current_branch}', expected 'urgent-fix-branch'."

    file_a = sandbox_dir / "file_a.txt"
    if not file_a.exists() or file_a.read_text() != FIXED_A:
        return False, "file_a.txt on urgent-fix-branch doesn't have the urgent fix applied."

    file_b = sandbox_dir / "file_b.txt"
    if not file_b.exists() or file_b.read_text() != ORIGINAL_B:
        return False, "file_b.txt on urgent-fix-branch should still be unmodified -- only the urgent-fix stash belongs here."

    main_a = run_git(sandbox_dir, ["show", "main:file_a.txt"], check=False)
    if main_a.returncode != 0 or main_a.stdout != ORIGINAL_A:
        return False, "main's committed file_a.txt changed -- the fix should have only ever lived in a stash, not a commit on main."

    stash_list = run_git(sandbox_dir, ["stash", "list"]).stdout.strip().splitlines()
    if len(stash_list) != 1:
        return False, f"expected exactly 1 stash remaining (wip-feature), found {len(stash_list)}."
    if "wip-feature" not in stash_list[0]:
        return False, f"the remaining stash isn't 'wip-feature': {stash_list[0]}"

    return True, "urgent-fix is applied on its own branch, and wip-feature is still safely stashed."
