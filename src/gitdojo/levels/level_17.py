"""Level 17 -- Git LFS."""

from pathlib import Path

from gitdojo.sandbox import run_git

ID = 17
TITLE = "Git LFS"
CATEGORY = "Config"

PROMPT = """\
Track *.bin files with Git LFS, then add and commit asset.bin (any
content). What actually gets committed to git's own history should be a
small LFS pointer file, not asset.bin's real content -- the real bytes
live in LFS storage instead, checked out via a smudge filter.
"""

HINTS = [
    "Git LFS works by registering clean/smudge filters for matching "
    "paths via .gitattributes -- `git lfs track` writes that for you. If "
    "commits still contain the raw file, LFS may not be initialized for "
    "this repo yet (`git lfs install`).",
    'Try: git lfs install ; git lfs track "*.bin" ; then add and commit '
    ".gitattributes and asset.bin.",
]

CANONICAL = (
    "git lfs install\n"
    'git lfs track "*.bin"\n'
    'echo "some binary-ish content" > asset.bin\n'
    "git add .gitattributes asset.bin\n"
    'git commit -m "Track and add binary asset via LFS"'
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])
    (sandbox_dir / "README.md").write_text("# project\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Initial commit"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    attrs = sandbox_dir / ".gitattributes"
    if not attrs.exists() or "filter=lfs" not in attrs.read_text():
        return False, "no LFS tracking configured for *.bin in .gitattributes."

    asset = sandbox_dir / "asset.bin"
    if not asset.exists():
        return False, "asset.bin doesn't exist in the working tree."

    blob = run_git(sandbox_dir, ["show", "HEAD:asset.bin"], check=False)
    if blob.returncode != 0:
        return False, "asset.bin isn't committed yet."
    if "git-lfs.github.com/spec" not in blob.stdout:
        return False, (
            "asset.bin's committed content isn't an LFS pointer -- make sure "
            "`git lfs track \"*.bin\"` (and `git lfs install`) ran before "
            "asset.bin was added, so the clean filter could intercept it."
        )

    return True, "asset.bin is tracked by LFS -- the commit holds a pointer, not the raw content."
