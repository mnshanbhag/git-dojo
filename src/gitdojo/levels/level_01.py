"""Level 1 -- Plumbing: content-addressing with hash-object."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 1
TITLE = "Plumbing basics: content-addressing"
CATEGORY = "Internals"

PROMPT = """\
There's a file called mystery.txt in this sandbox. Without opening it in
an editor, use a git plumbing command to compute its git object SHA-1, and
write *just* that 40-character SHA (nothing else) into a new file called
answer.txt, in this same directory.
"""

HINTS = [
    "This is about content-addressing: git can compute the SHA-1 an object "
    "would get from a file's raw bytes, without the file being added or "
    "committed to anything.",
    "Try: git hash-object mystery.txt -- then redirect that output into "
    "answer.txt.",
]

CANONICAL = "git hash-object mystery.txt > answer.txt"

MYSTERY_CONTENT = "the taste of a byte\n"


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q"])
    (sandbox_dir / "mystery.txt").write_text(MYSTERY_CONTENT)


def check(sandbox_dir: Path) -> tuple[bool, str]:
    answer_file = sandbox_dir / "answer.txt"
    if not answer_file.exists():
        return False, "answer.txt doesn't exist yet."

    given = answer_file.read_text().strip()

    mystery_file = sandbox_dir / "mystery.txt"
    if not mystery_file.exists():
        return False, "mystery.txt is missing from the sandbox -- don't delete it."

    expected = run_git(sandbox_dir, ["hash-object", "mystery.txt"]).stdout.strip()

    if given == expected:
        return True, "That's the correct blob SHA-1 for mystery.txt's content."

    if len(given) != 40 or not all(c in "0123456789abcdef" for c in given.lower()):
        return False, f"answer.txt contains '{given}', which isn't a 40-character SHA-1 at all."

    return False, f"answer.txt contains '{given}', but that doesn't match mystery.txt's actual object hash."
