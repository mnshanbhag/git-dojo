"""Level 25 -- Release engineering: semver tags + auto-generated notes."""

import json
from pathlib import Path

from gitdojo.sandbox import run_gh, run_git

ID = 25
TITLE = "Release engineering: semver tag + release notes"
CATEGORY = "GitHub"

PRACTICE_REPO = "mnshanbhag/git-dojo-gh-practice"
PRACTICE_REPO_URL = f"https://github.com/{PRACTICE_REPO}.git"
TAG = "v1.0.0"

PROMPT = f"""\
In this practice repo clone, tag the current commit with an annotated
semver tag, {TAG}, push it, then create a GitHub Release from that tag
with auto-generated release notes (based on commits since the last tag).
"""

HINTS = [
    "An annotated tag (git tag -a, or -m which implies it) carries its "
    "own message/author, unlike a lightweight tag which is just a pointer "
    "-- releases are built from these. `gh release create` can generate "
    "notes for you from the commit history instead of writing them by hand.",
    f'Try: git tag -a {TAG} -m "Release {TAG}" ; git push origin {TAG} ; '
    f"gh release create {TAG} --repo {PRACTICE_REPO} --generate-notes",
]

CANONICAL = (
    f'git tag -a {TAG} -m "Release {TAG}"\n'
    f"git push origin {TAG}\n"
    f"gh release create {TAG} --repo {PRACTICE_REPO} --generate-notes"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["clone", PRACTICE_REPO_URL, "."], check=False)
    run_git(sandbox_dir, ["config", "user.email", "mnshanbhag@gmail.com"])
    run_git(sandbox_dir, ["config", "user.name", "mnshanbhag"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    tag_check = run_gh(["api", f"repos/{PRACTICE_REPO}/git/refs/tags/{TAG}"])
    if tag_check.returncode != 0:
        return False, f"tag {TAG} doesn't exist on GitHub yet -- push it."

    release = run_gh(
        ["release", "view", TAG, "--repo", PRACTICE_REPO, "--json", "tagName,body"]
    )
    if release.returncode != 0:
        return False, f"no GitHub Release found for {TAG} yet -- create one."

    info = json.loads(release.stdout)
    if not info.get("body", "").strip():
        return False, "the release exists but has no notes -- use --generate-notes (or write some)."

    return True, f"{TAG} is tagged, released, and has non-empty release notes."
