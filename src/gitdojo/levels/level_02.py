"""Level 2 -- Diff & blame mastery: git blame --ignore-rev."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 2
TITLE = "Diff & blame mastery: blame --ignore-rev"
CATEGORY = "Internals"

PROMPT = """\
poem.txt has three lines. The first two were written in one commit, then
a later commit reformatted the whole file (added leading indentation to
every line) without changing its meaning. A third line was then added
normally.

Plain `git blame poem.txt` blames that reformat commit for lines 1 and 2,
which is useless -- it wasn't the reformat commit that actually wrote
that text. Find out which commit *really* introduced line 1 ("roses are
red"), by having blame skip over the reformat commit, and write that
commit's SHA (full or abbreviated, at least 7 characters) into answer.txt.
"""

HINTS = [
    "There's a git blame flag that lets you tell git to pretend a specific "
    "commit never happened when deciding who's responsible for a line -- "
    "useful exactly for mass-reformatting commits.",
    "Find the reformat commit's SHA with `git log --oneline poem.txt`, then "
    "run: git blame --ignore-rev <that-sha> poem.txt -- read off the SHA "
    "shown for line 1.",
]

CANONICAL = (
    "git log --oneline -- poem.txt   # find the reformat commit's SHA\n"
    "git blame --ignore-rev <reformat-sha> poem.txt   # read line 1's real SHA\n"
    "echo <that-sha> > answer.txt"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "poem.txt").write_text("roses are red\nviolets are blue\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add poem"])

    (sandbox_dir / "poem.txt").write_text("  roses are red\n  violets are blue\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Reformat: normalize indentation"])

    (sandbox_dir / "poem.txt").write_text(
        "  roses are red\n  violets are blue\n  sugar is sweet\n"
    )
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add third line"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    answer_file = sandbox_dir / "answer.txt"
    if not answer_file.exists():
        return False, "answer.txt doesn't exist yet."

    given = answer_file.read_text().strip().lstrip("^").lower()

    history = run_git(
        sandbox_dir, ["log", "--format=%H", "--follow", "--", "poem.txt"]
    ).stdout.strip().splitlines()
    if not history:
        return False, "poem.txt has no history -- don't delete or recreate it."
    expected = history[-1].lower()

    if len(given) < 7:
        return False, f"'{given}' is too short to be a meaningful commit SHA."

    if expected.startswith(given):
        return True, "That's the commit that really introduced line 1."

    return False, f"'{given}' doesn't match the commit that introduced line 1."
