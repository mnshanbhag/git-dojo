"""Level 7 -- git bisect (manual + bisect run)."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 7
TITLE = "git bisect"
CATEGORY = "History"

CHECK_SCRIPT = (
    "import calc\n"
    'assert calc.add(2, 3) == 5, "add() is broken"\n'
    'print("OK")\n'
)

PROMPT = """\
calc.py's add() function used to work correctly. Somewhere along the way,
a commit disguised as an innocuous refactor silently broke it, and HEAD
is now bad.

check.py (present from the "Implement add()" commit onward) will tell you
pass/fail for any commit from that point on -- run `python check.py`
yourself, or let git drive the whole search with
`git bisect run python check.py`.

Known good: the "Implement add()" commit itself was fine.
Known bad: HEAD.

Find the exact commit that introduced the bug, write its full commit SHA
into answer.txt, and don't forget to `git bisect reset` when you're done.
"""

HINTS = [
    "git bisect does a binary search between a known-good and known-bad "
    "commit, checking out a candidate each step for you (or a script) to "
    "test.",
    "Try: git bisect start; git bisect bad HEAD; "
    "git bisect good <sha-of-'Implement add()'>; then "
    "git bisect run python check.py -- git will report the first bad "
    "commit directly. Finish with git bisect reset.",
]

CANONICAL = (
    "git bisect start\n"
    "git bisect bad HEAD\n"
    "git bisect good <sha of 'Implement add()'>\n"
    "git bisect run python check.py\n"
    "echo <reported-sha> > answer.txt\n"
    "git bisect reset"
)

BUG_COMMIT_MESSAGE = "Refactor add() internals"


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "check.py").write_text(CHECK_SCRIPT)
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add check script"])

    (sandbox_dir / "calc.py").write_text("def add(a, b):\n    return a + b\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Implement add()"])

    (sandbox_dir / "calc.py").write_text(
        "def add(a, b):\n    return a + b\n\n\ndef subtract(a, b):\n    return a - b\n"
    )
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add subtract()"])

    (sandbox_dir / "calc.py").write_text(
        "def add(a, b):\n    return a + b + 1\n\n\ndef subtract(a, b):\n    return a - b\n"
    )
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", BUG_COMMIT_MESSAGE])

    (sandbox_dir / "calc.py").write_text(
        "def add(a, b):\n    return a + b + 1\n\n\n"
        "def subtract(a, b):\n    return a - b\n\n\n"
        "def multiply(a, b):\n    return a * b\n"
    )
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add multiply()"])

    (sandbox_dir / "calc.py").write_text(
        'def add(a, b):\n    """Add two numbers."""\n    return a + b + 1\n\n\n'
        "def subtract(a, b):\n    return a - b\n\n\n"
        "def multiply(a, b):\n    return a * b\n"
    )
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Update docstrings"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    if (sandbox_dir / ".git" / "BISECT_LOG").exists():
        return False, "looks like a bisect is still in progress -- finish with `git bisect reset`."

    answer_file = sandbox_dir / "answer.txt"
    if not answer_file.exists():
        return False, "answer.txt doesn't exist yet."

    given = answer_file.read_text().strip().lstrip("^").lower()
    if len(given) < 7:
        return False, f"'{given}' is too short to be a meaningful commit SHA."

    matches = run_git(
        sandbox_dir, ["log", "--all", "--format=%H", "--grep=^" + BUG_COMMIT_MESSAGE + "$"]
    ).stdout.strip().splitlines()
    if not matches:
        return False, "couldn't find the expected bug commit in history -- don't rewrite history here."
    expected = matches[0].lower()

    if expected.startswith(given):
        return True, "That's the commit that broke add()."

    return False, f"'{given}' isn't the commit that introduced the bug."
