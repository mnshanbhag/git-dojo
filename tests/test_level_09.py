from gitdojo.levels import level_09
from gitdojo.sandbox import run_git


def solve(tmp_path):
    run_git(tmp_path, ["config", "rerere.enabled", "true"])
    run_git(tmp_path, ["merge", "feature-a"], check=False)
    (tmp_path / "config.txt").write_text("key=value_from_main\n")
    run_git(tmp_path, ["add", "config.txt"])
    run_git(tmp_path, ["commit", "-q", "--no-edit"])
    run_git(tmp_path, ["reset", "-q", "--hard", "HEAD^"])
    run_git(tmp_path, ["merge", "feature-a"], check=False)
    run_git(tmp_path, ["add", "config.txt"])
    run_git(tmp_path, ["commit", "-q", "--no-edit"])


def test_check_fails_before_merge(tmp_path):
    level_09.setup(tmp_path)
    ok, message = level_09.check(tmp_path)
    assert not ok


def test_check_passes_after_rerere_replay(tmp_path):
    level_09.setup(tmp_path)
    solve(tmp_path)
    ok, message = level_09.check(tmp_path)
    assert ok
    assert (tmp_path / "config.txt").read_text() == "key=value_from_main\n"
