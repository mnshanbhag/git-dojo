"""Level 18 -- Signing: SSH-based commit and tag signing."""

import subprocess
from pathlib import Path

from gitdojo.sandbox import run_git

ID = 18
TITLE = "Signing: SSH commits and tags"
CATEGORY = "Config"

PROMPT = """\
There's an SSH keypair at signing_key / signing_key.pub in this sandbox,
and an allowed_signers file already listing that public key for
verification.

Configure git to sign with SSH using this key, then:
1. Make HEAD a signed commit (amend it, or create a new signed commit).
2. Create a signed, annotated tag called "v1.0" on it.

Both must pass `git verify-commit` / `git verify-tag`.
"""

HINTS = [
    "Signing isn't GPG-only -- git can sign with an SSH key instead by "
    "setting gpg.format to ssh and pointing user.signingkey at a public "
    "key file. Verification needs to know which keys are trusted, via "
    "gpg.ssh.allowedSignersFile.",
    "Try: git config gpg.format ssh ; git config user.signingkey "
    "./signing_key.pub ; git config gpg.ssh.allowedSignersFile "
    "./allowed_signers ; git commit --amend -S --no-edit ; "
    'git tag -s v1.0 -m "Release 1.0"',
]

CANONICAL = (
    "git config gpg.format ssh\n"
    "git config user.signingkey ./signing_key.pub\n"
    "git config gpg.ssh.allowedSignersFile ./allowed_signers\n"
    "git commit --amend -S --no-edit\n"
    'git tag -s v1.0 -m "Release 1.0"'
)


def setup(sandbox_dir: Path) -> None:
    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])
    (sandbox_dir / "file.txt").write_text("content\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "Initial commit"])

    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", "signing_key", "-N", "", "-q"],
        cwd=sandbox_dir,
        check=True,
    )
    pubkey = (sandbox_dir / "signing_key.pub").read_text().strip()
    (sandbox_dir / "allowed_signers").write_text(f"dojo@example.com {pubkey}\n")


def check(sandbox_dir: Path) -> tuple[bool, str]:
    commit_verify = run_git(sandbox_dir, ["verify-commit", "HEAD"], check=False)
    if commit_verify.returncode != 0:
        return False, "HEAD isn't a verifiable signed commit yet."

    tag_verify = run_git(sandbox_dir, ["verify-tag", "v1.0"], check=False)
    if tag_verify.returncode != 0:
        return False, "tag 'v1.0' doesn't exist or isn't a verifiable signed tag."

    tag_target = run_git(sandbox_dir, ["rev-list", "-n", "1", "v1.0"], check=False).stdout.strip()
    head = run_git(sandbox_dir, ["rev-parse", "HEAD"]).stdout.strip()
    if tag_target != head:
        return False, "v1.0 doesn't point at HEAD."

    return True, "HEAD is a verified signed commit, and v1.0 is a verified signed tag pointing at it."
