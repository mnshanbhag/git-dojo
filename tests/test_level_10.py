from gitdojo.levels import level_10
from gitdojo.sandbox import run_git


def test_check_fails_before_cherry_pick(tmp_path):
    level_10.setup(tmp_path)
    ok, message = level_10.check(tmp_path)
    assert not ok


def test_check_passes_after_cherry_pick(tmp_path):
    level_10.setup(tmp_path)
    fix_sha = run_git(
        tmp_path, ["log", "--format=%H", "--grep=^Fix greeting typo$"]
    ).stdout.strip()
    run_git(tmp_path, ["checkout", "-q", "release-1.0"])
    run_git(tmp_path, ["cherry-pick", fix_sha])
    ok, message = level_10.check(tmp_path)
    assert ok


def test_check_fails_if_unrelated_commit_also_picked(tmp_path):
    level_10.setup(tmp_path)
    fix_sha = run_git(
        tmp_path, ["log", "--format=%H", "--grep=^Fix greeting typo$"]
    ).stdout.strip()
    extra_sha = run_git(
        tmp_path, ["log", "--format=%H", "--grep=^Add unrelated main-only feature$"]
    ).stdout.strip()
    run_git(tmp_path, ["checkout", "-q", "release-1.0"])
    run_git(tmp_path, ["cherry-pick", fix_sha, extra_sha])
    ok, message = level_10.check(tmp_path)
    assert not ok
