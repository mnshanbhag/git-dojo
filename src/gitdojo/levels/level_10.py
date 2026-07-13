"""Level 10 -- Cherry-pick backport."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 10
TITLE = "Cherry-pick backport"
CATEGORY = "Branching"

PROMPT = """\
main has two commits since release-1.0 branched off: "Fix greeting typo"
(a real bug fix that should ship in the release too) and "Add unrelated
main-only feature" (which should NOT go into the release).

Backport just the fix onto release-1.0, without bringing along the
unrelated feature.
"""

HINTS = [
    "There's a command that replays a single existing commit onto your "
    "current branch, without needing to merge or rebase everything else "
    "along with it.",
    "Try: git log --oneline main (find the fix's SHA), then "
    "git checkout release-1.0 && git cherry-pick <that-sha>.",
]

CANONICAL = (
    "git log --oneline main            # find the fix commit's SHA\n"
    "git checkout release-1.0\n"
    "git cherry-pick <fix-sha>"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "app.py").write_text('def greet():\n    return "Hello"\n')
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "v1.0 base"])

    run_git(sandbox_dir, ["checkout", "-q", "-b", "release-1.0"])
    run_git(sandbox_dir, ["checkout", "-q", "main"])

    (sandbox_dir / "app.py").write_text('def greet():\n    return "Hello!"\n')
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Fix greeting typo"])

    (sandbox_dir / "extra_feature.py").write_text("def new_feature():\n    pass\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Add unrelated main-only feature"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    app = run_git(sandbox_dir, ["show", "release-1.0:app.py"], check=False)
    if app.returncode != 0:
        return False, "release-1.0 branch or app.py on it is missing."
    if "Hello!" not in app.stdout:
        return False, "the fix isn't present on release-1.0 yet."

    files = run_git(
        sandbox_dir, ["ls-tree", "-r", "--name-only", "release-1.0"]
    ).stdout
    if "extra_feature.py" in files:
        return False, "the unrelated main-only commit leaked onto release-1.0."

    count = run_git(sandbox_dir, ["rev-list", "--count", "release-1.0"]).stdout.strip()
    if count != "2":
        return False, f"expected exactly 2 commits on release-1.0, found {count}."

    return True, "release-1.0 has just the backported fix, nothing else from main."
