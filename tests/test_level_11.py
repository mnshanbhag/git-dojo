from gitdojo.levels import level_11
from gitdojo.sandbox import run_git


def test_check_fails_before_merges(tmp_path):
    level_11.setup(tmp_path)
    ok, message = level_11.check(tmp_path)
    assert not ok


def test_check_passes_after_theirs_and_octopus_merge(tmp_path):
    level_11.setup(tmp_path)
    run_git(tmp_path, ["merge", "-X", "theirs", "hotfix", "-q", "-m", "Merge hotfix"])
    run_git(tmp_path, ["merge", "b1", "b2", "b3", "-q", "-m", "Octopus merge features"])
    ok, message = level_11.check(tmp_path)
    assert ok


def test_check_fails_if_merged_separately_not_octopus(tmp_path):
    level_11.setup(tmp_path)
    run_git(tmp_path, ["merge", "-X", "theirs", "hotfix", "-q", "-m", "Merge hotfix"])
    run_git(tmp_path, ["merge", "b1", "-q", "-m", "Merge b1"])
    run_git(tmp_path, ["merge", "b2", "-q", "-m", "Merge b2"])
    run_git(tmp_path, ["merge", "b3", "-q", "-m", "Merge b3"])
    ok, message = level_11.check(tmp_path)
    assert not ok
