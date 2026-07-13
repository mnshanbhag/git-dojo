"""Level 16 -- .gitattributes: union merge driver."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 16
TITLE = ".gitattributes: union merge driver"
CATEGORY = "Config"

PROMPT = """\
main and feature both added a different line to CHANGELOG.txt right
after the same base line -- a real conflict under a normal merge.

Set up a union merge for CHANGELOG.txt via .gitattributes (git ships a
built-in `union` merge driver -- no custom script needed), then merge
feature into main. It should auto-resolve with both new lines present,
no conflict markers, and no manual editing.
"""

HINTS = [
    "A merge driver is chosen per-path via .gitattributes, using "
    "`<pattern> merge=<driver>`. git has a built-in driver named `union` "
    "that keeps both sides' added lines instead of conflicting on them.",
    'Try: echo "CHANGELOG.txt merge=union" > .gitattributes -- then: '
    "git merge feature -m \"Merge feature\"",
]

CANONICAL = (
    'echo "CHANGELOG.txt merge=union" > .gitattributes\n'
    'git merge feature -m "Merge feature"'
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "CHANGELOG.txt").write_text("- Initial release\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Initial changelog"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "feature"])
    (sandbox_dir / "CHANGELOG.txt").write_text("- Initial release\n- Feature X added\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add feature X changelog entry"])

    run_git(sandbox_dir, ["checkout", "-q", "main"])
    (sandbox_dir / "CHANGELOG.txt").write_text("- Initial release\n- Bug Y fixed\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add bugfix changelog entry"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    attrs = sandbox_dir / ".gitattributes"
    if not attrs.exists() or "merge=union" not in attrs.read_text():
        return False, "no union merge driver configured for CHANGELOG.txt in .gitattributes."

    changelog = sandbox_dir / "CHANGELOG.txt"
    if not changelog.exists():
        return False, "CHANGELOG.txt is missing."
    content = changelog.read_text()

    if "<<<<<<<" in content:
        return False, "CHANGELOG.txt still has conflict markers -- the merge wasn't auto-resolved."
    if "- Feature X added" not in content or "- Bug Y fixed" not in content:
        return False, "CHANGELOG.txt is missing one of the two branches' new lines."

    merges = run_git(sandbox_dir, ["log", "--merges", "--format=%H", "main"]).stdout.strip()
    if not merges:
        return False, "no merge commit found on main."

    return True, "feature merged cleanly via the union driver -- both changelog entries kept, no conflict."
