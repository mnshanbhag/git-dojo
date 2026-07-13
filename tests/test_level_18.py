from gitdojo.levels import level_18
from gitdojo.sandbox import run_git


def solve(tmp_path):
    run_git(tmp_path, ["config", "gpg.format", "ssh"])
    run_git(tmp_path, ["config", "user.signingkey", "./signing_key.pub"])
    run_git(tmp_path, ["config", "gpg.ssh.allowedSignersFile", "./allowed_signers"])
    run_git(tmp_path, ["commit", "--amend", "-S", "--no-edit", "-q"])
    run_git(tmp_path, ["tag", "-s", "v1.0", "-m", "Release 1.0"])


def test_check_fails_before_signing(tmp_path):
    level_18.setup(tmp_path)
    ok, message = level_18.check(tmp_path)
    assert not ok


def test_check_passes_after_ssh_signing(tmp_path):
    level_18.setup(tmp_path)
    solve(tmp_path)
    ok, message = level_18.check(tmp_path)
    assert ok


def test_check_fails_if_tag_not_signed(tmp_path):
    level_18.setup(tmp_path)
    run_git(tmp_path, ["config", "gpg.format", "ssh"])
    run_git(tmp_path, ["config", "user.signingkey", "./signing_key.pub"])
    run_git(tmp_path, ["config", "gpg.ssh.allowedSignersFile", "./allowed_signers"])
    run_git(tmp_path, ["commit", "--amend", "-S", "--no-edit", "-q"])
    run_git(tmp_path, ["tag", "v1.0", "-m", "Release 1.0"])
    ok, message = level_18.check(tmp_path)
    assert not ok
