from gitdojo.levels import level_05
from gitdojo.sandbox import run_git


def test_check_fails_before_rebase(tmp_path):
    level_05.setup(tmp_path)
    ok, message = level_05.check(tmp_path)
    assert not ok
    assert "staging is still an ancestor" in message


def test_check_passes_after_rebase_onto(tmp_path):
    level_05.setup(tmp_path)
    run_git(tmp_path, ["rebase", "--onto", "main", "staging", "feature"])
    ok, message = level_05.check(tmp_path)
    assert ok
