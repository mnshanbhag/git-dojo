"""Level 21 -- format-patch / git am: email-style patch workflow."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 21
TITLE = "format-patch / git am"
CATEGORY = "Exchange"

PROMPT = """\
feature has two commits on top of main ("Add util function", "Use util
function") that never got merged anywhere -- imagine they need to travel
to a repo with no shared remote, the old-fashioned way: as patch files
over email.

Generate them as patch files with `git format-patch` into a `patches/`
directory, then apply those patch files onto the `target` branch (which
also branched from main, but never saw feature's work) with `git am`.
"""

HINTS = [
    "`git format-patch <range>` turns a range of commits into one .patch "
    "file per commit, each a plain-text email with the diff attached. "
    "`git am` on the other end reads those files back in and creates "
    "real commits from them, preserving the author and message.",
    "Try: git format-patch main..feature -o patches -- then: "
    "git checkout target && git am patches/*.patch",
]

CANONICAL = (
    "git format-patch main..feature -o patches\n"
    "git checkout target\n"
    "git am patches/*.patch"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "README.md").write_text("base\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Base"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "feature"])
    (sandbox_dir / "utils.py").write_text("def util(): return 1\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add util function"])
    (sandbox_dir / "README.md").write_text("base\nfrom utils import util\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Use util function"])

    run_git(sandbox_dir, ["checkout", "-q", "main"])
    run_git(sandbox_dir, ["checkout", "-q", "-b", "target"])
    run_git(sandbox_dir, ["checkout", "-q", "main"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    patches_dir = sandbox_dir / "patches"
    if not patches_dir.exists() or not list(patches_dir.glob("*.patch")):
        return False, "no .patch files found in patches/ -- run git format-patch first."

    messages = run_git(
        sandbox_dir, ["log", "--format=%s", "--reverse", "main..target"]
    ).stdout.strip().splitlines()
    expected = ["Add util function", "Use util function"]
    if messages != expected:
        return False, f"target's commits past main are {messages}, expected {expected}."

    utils_content = run_git(sandbox_dir, ["show", "target:utils.py"], check=False)
    if utils_content.returncode != 0 or "util" not in utils_content.stdout:
        return False, "target:utils.py is missing or doesn't match feature's version."

    return True, "target now has feature's two commits, applied from patch files via git am."
