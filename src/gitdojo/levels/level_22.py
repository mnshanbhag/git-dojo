"""Level 22 -- git bundle / git archive."""

import tarfile
from pathlib import Path

from gitdojo.sandbox import run_git

ID = 22
TITLE = "git bundle / git archive"
CATEGORY = "Exchange"

PROMPT = """\
Two things you might need without any server in the picture:

1. Export this entire repo to a single file, repo.bundle, containing all
   of main's history -- as if handing the whole repo to someone offline.
2. Export just the current snapshot (no history) to a tar file,
   release.tar, via git archive -- e.g. for shipping a release tarball.
"""

HINTS = [
    "`git bundle create <file> <refs>` packs commits and refs into one "
    "portable file that git bundle verify / git clone can read back like "
    "a remote. `git archive` instead exports a *snapshot* of one tree -- "
    "no history, no .git directory, just the files.",
    "Try: git bundle create repo.bundle --all -- then: "
    "git archive --format=tar -o release.tar HEAD",
]

CANONICAL = (
    "git bundle create repo.bundle --all\n"
    "git archive --format=tar -o release.tar HEAD"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])

    (sandbox_dir / "README.md").write_text("# project\n")
    (sandbox_dir / "app.py").write_text("app = True\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Initial commit"])

    (sandbox_dir / "app.py").write_text("app = True\nversion = 2\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Update app"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    bundle_file = sandbox_dir / "repo.bundle"
    if not bundle_file.exists():
        return False, "repo.bundle doesn't exist yet."

    verify = run_git(sandbox_dir, ["bundle", "verify", "repo.bundle"], check=False)
    if verify.returncode != 0:
        return False, "repo.bundle exists but doesn't verify as a valid bundle."

    archive_file = sandbox_dir / "release.tar"
    if not archive_file.exists():
        return False, "release.tar doesn't exist yet."

    try:
        with tarfile.open(archive_file) as tf:
            names = tf.getnames()
    except tarfile.TarError:
        return False, "release.tar isn't a valid tar archive."

    if "README.md" not in names or "app.py" not in names:
        return False, f"release.tar is missing expected files, found: {names}"

    return True, "repo.bundle verifies as a complete bundle, and release.tar has the right files."
