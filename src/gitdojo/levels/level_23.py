"""Level 23 -- Branch protection + CODEOWNERS + required status checks.

Unlike every other level, this one runs against a real, disposable GitHub
repo (git-dojo-gh-practice) instead of a purely local sandbox, since
branch protection and CODEOWNERS only mean anything server-side.

check() only ever reads GitHub state (gh api GET calls). It never
configures branch protection itself -- that's an access-control change,
and the trainer's whole model is "you run the real command, we verify
the result" anyway. You do this one through the GitHub UI or your own
`gh api` calls.
"""

from pathlib import Path

from gitdojo.sandbox import run_gh, run_git

ID = 23
TITLE = "Branch protection + CODEOWNERS + required status checks"
CATEGORY = "GitHub"

PRACTICE_REPO = "mnshanbhag/git-dojo-gh-practice"
PRACTICE_REPO_URL = f"https://github.com/{PRACTICE_REPO}.git"

PROMPT = f"""\
This level uses a real, disposable GitHub repo -- {PRACTICE_REPO} --
cloned into this sandbox. gitdojo checks the repo's actual settings on
GitHub, not just your local clone, so you need to push.

1. Add .github/CODEOWNERS to this repo assigning yourself as owner of
   everything (one line: `* @mnshanbhag`), commit, and push.
2. On GitHub (Settings > Branches, or `gh api` yourself), add a branch
   protection rule for `main` that requires at least one status check
   to pass before merging -- any check name works, it doesn't need to
   correspond to a real workflow.
"""

HINTS = [
    "CODEOWNERS is just a file (.github/CODEOWNERS) -- push it like "
    "anything else. Branch protection and required status checks are a "
    "repo *setting*, not a file -- configure it in Settings > Branches > "
    "Branch protection rules on GitHub, or via `gh api --method PUT "
    "repos/{owner}/{repo}/branches/main/protection` yourself.",
    "The CODEOWNERS line format is `<pattern> <owner>`, e.g. `* @mnshanbhag` "
    "for \"this user owns everything\". For protection, the API needs "
    "required_status_checks with a non-empty contexts list, plus "
    "required_pull_request_reviews and enforce_admins (can be null/false).",
]

CANONICAL = (
    "echo '* @mnshanbhag' > .github/CODEOWNERS\n"
    "git add .github/CODEOWNERS && git commit -m 'Add CODEOWNERS' && git push\n"
    "# then, on GitHub: Settings > Branches > Add branch protection rule for main,\n"
    "# check 'Require status checks to pass before merging', add a check name."
)


def setup(sandbox_dir: Path) -> None:
    exists = run_gh(["repo", "view", PRACTICE_REPO, "--json", "name"])
    if exists.returncode != 0:
        run_gh(
            [
                "repo", "create", PRACTICE_REPO, "--public",
                "--description", "Disposable practice repo for git-dojo's GitHub-platform levels",
            ],
            check=True,
        )

    run_git(sandbox_dir, ["clone", PRACTICE_REPO_URL, "."], check=False)
    if not (sandbox_dir / ".git").exists():
        # Empty remote (brand new repo): init and push a base commit instead.
        run_git(sandbox_dir, ["init", "-q", "-b", "main"])
        run_git(sandbox_dir, ["remote", "add", "origin", PRACTICE_REPO_URL])
        (sandbox_dir / "README.md").write_text("# git-dojo-gh-practice\n\nDisposable practice repo.\n")
        run_git(sandbox_dir, ["add", "."])
        run_git(sandbox_dir, ["config", "user.email", "mnshanbhag@gmail.com"])
        run_git(sandbox_dir, ["config", "user.name", "mnshanbhag"])
        run_git(sandbox_dir, ["commit", "-q", "-m", "Initial commit"])
        run_git(sandbox_dir, ["push", "-u", "origin", "main"])

    run_git(sandbox_dir, ["config", "user.email", "mnshanbhag@gmail.com"])
    run_git(sandbox_dir, ["config", "user.name", "mnshanbhag"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    codeowners = run_gh(["api", f"repos/{PRACTICE_REPO}/contents/.github/CODEOWNERS"])
    if codeowners.returncode != 0:
        return False, "no .github/CODEOWNERS found on GitHub yet -- commit and push it."

    protection = run_gh(["api", f"repos/{PRACTICE_REPO}/branches/main/protection"])
    if protection.returncode != 0:
        return False, "main isn't protected yet -- add a branch protection rule on GitHub."

    contexts = run_gh(
        ["api", f"repos/{PRACTICE_REPO}/branches/main/protection/required_status_checks", "--jq", ".contexts"]
    )
    if contexts.returncode != 0 or contexts.stdout.strip() in ("", "[]", "null"):
        return False, "main is protected, but no required status checks are configured yet."

    return True, "CODEOWNERS is in place, and main requires status checks to merge."
