"""Level 24 -- GitHub Actions: matrix builds.

Runs against the same disposable practice repo as level 23. check() reads
the latest workflow run via `gh run` -- read-only, same as level 23.
"""

import json
from pathlib import Path

from gitdojo.sandbox import run_gh, run_git

ID = 24
TITLE = "GitHub Actions: matrix builds"
CATEGORY = "GitHub"

PRACTICE_REPO = "mnshanbhag/git-dojo-gh-practice"
PRACTICE_REPO_URL = f"https://github.com/{PRACTICE_REPO}.git"
WORKFLOW_FILE = "ci-matrix.yml"

PROMPT = f"""\
In this practice repo clone, add a GitHub Actions workflow at
.github/workflows/{WORKFLOW_FILE}, triggered on push, with a build job
that runs across a matrix with at least two axes and two values each
(e.g. a "version" axis and a "flavor" axis) -- 4 jobs total. Push it,
wait about 30 seconds for it to run, then check.
"""

HINTS = [
    "A workflow's `jobs.<id>.strategy.matrix` takes arbitrary named axes, "
    "each with a list of values -- GitHub runs one job per *combination*, "
    "so two 2-value axes means 4 jobs.",
    'Try a workflow with:\n'
    '  jobs:\n'
    '    build:\n'
    '      runs-on: ubuntu-latest\n'
    '      strategy:\n'
    '        matrix:\n'
    '          version: [1, 2]\n'
    '          flavor: [a, b]\n'
    '      steps:\n'
    '        - run: echo "${{ matrix.version }} ${{ matrix.flavor }}"',
]

CANONICAL = f"""\
mkdir -p .github/workflows
cat > .github/workflows/{WORKFLOW_FILE} << 'EOF'
name: ci-matrix
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        version: [1, 2]
        flavor: [a, b]
    steps:
      - run: echo "${{{{ matrix.version }}}} ${{{{ matrix.flavor }}}}"
EOF
git add .github/workflows/{WORKFLOW_FILE}
git commit -m "Add matrix CI workflow"
git push"""


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["clone", PRACTICE_REPO_URL, "."], check=False)
    run_git(sandbox_dir, ["config", "user.email", "mnshanbhag@gmail.com"])
    run_git(sandbox_dir, ["config", "user.name", "mnshanbhag"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    runs = run_gh(
        [
            "run", "list", "--repo", PRACTICE_REPO,
            "--workflow", WORKFLOW_FILE, "--limit", "1",
            "--json", "databaseId,status,conclusion",
        ]
    )
    if runs.returncode != 0 or runs.stdout.strip() in ("", "[]"):
        return False, f"no runs found for {WORKFLOW_FILE} yet -- push it and wait a bit."

    run_info = json.loads(runs.stdout)[0]
    if run_info["status"] != "completed":
        return False, "the latest run hasn't finished yet -- wait a bit and check again."
    if run_info["conclusion"] != "success":
        return False, f"the latest run's conclusion was '{run_info['conclusion']}', expected success."

    jobs = run_gh(
        ["run", "view", str(run_info["databaseId"]), "--repo", PRACTICE_REPO, "--json", "jobs"]
    )
    if jobs.returncode != 0:
        return False, "couldn't fetch jobs for the latest run."

    job_count = len(json.loads(jobs.stdout)["jobs"])
    if job_count < 4:
        return False, f"the run had {job_count} job(s), expected at least 4 (a 2x2 matrix)."

    return True, f"the matrix workflow ran successfully with {job_count} jobs."
