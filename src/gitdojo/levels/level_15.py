"""Level 15 -- Hooks: commit-msg enforcing Conventional Commits."""

import subprocess
from pathlib import Path

from gitdojo.sandbox import run_git

ID = 15
TITLE = "Hooks: commit-msg"
CATEGORY = "Config"

PROMPT = """\
Write a commit-msg hook at .git/hooks/commit-msg that rejects any commit
message not following Conventional Commits format: "type: description",
where type is one of feat, fix, chore, docs, refactor, test. Make it
executable.

The hook receives the path to a file containing the proposed commit
message as its first argument ($1), and should exit non-zero to reject
the commit.
"""

HINTS = [
    "Git hooks are just executable scripts in .git/hooks/ -- no special "
    "registration needed, just the right filename, executable bit, and a "
    "correct exit code (non-zero rejects the commit). The commit-msg hook "
    "gets one argument: the path to a temp file holding the message.",
    "Try a shell script like:\n"
    "  #!/bin/sh\n"
    "  grep -qE '^(feat|fix|chore|docs|refactor|test)(\\(.+\\))?: .+' \"$1\" "
    "|| exit 1\n"
    "saved to .git/hooks/commit-msg, then `chmod +x .git/hooks/commit-msg`.",
]

CANONICAL = (
    "cat > .git/hooks/commit-msg << 'EOF'\n"
    "#!/bin/sh\n"
    "grep -qE '^(feat|fix|chore|docs|refactor|test)(\\(.+\\))?: .+' \"$1\" || exit 1\n"
    "EOF\n"
    "chmod +x .git/hooks/commit-msg"
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])
    (sandbox_dir / "README.md").write_text("# project\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Initial commit"])


def _run_hook(hook_path: Path, sandbox_dir: Path, message: str) -> subprocess.CompletedProcess:
    msg_file = sandbox_dir / ".gitdojo-tmp-msg"
    msg_file.write_text(message)
    try:
        return subprocess.run(
            ["bash", str(hook_path), str(msg_file)],
            cwd=sandbox_dir,
            capture_output=True,
            text=True,
        )
    finally:
        msg_file.unlink(missing_ok=True)


def check(sandbox_dir: Path) -> tuple[bool, str]:
    hook_path = sandbox_dir / ".git" / "hooks" / "commit-msg"
    if not hook_path.exists():
        return False, "no commit-msg hook found at .git/hooks/commit-msg."

    bad = _run_hook(hook_path, sandbox_dir, "made some changes\n")
    if bad.returncode == 0:
        return False, "the hook accepted a non-conventional message ('made some changes') -- it should reject it."

    good = _run_hook(hook_path, sandbox_dir, "feat: add greeting\n")
    if good.returncode != 0:
        return False, "the hook rejected a valid Conventional Commits message ('feat: add greeting') -- it should accept it."

    return True, "the commit-msg hook correctly rejects non-conventional messages and accepts valid ones."
