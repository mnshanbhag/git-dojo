from gitdojo.levels import level_06
from gitdojo.sandbox import run_git


def test_check_fails_before_split(tmp_path):
    level_06.setup(tmp_path)
    ok, message = level_06.check(tmp_path)
    assert not ok


def split(tmp_path):
    run_git(
        tmp_path,
        ["-c", "sequence.editor=sed -i s/^pick/edit/", "rebase", "-i", "HEAD~1"],
    )
    run_git(tmp_path, ["reset", "HEAD^"])
    run_git(tmp_path, ["add", "utils.py"])
    run_git(tmp_path, ["commit", "-q", "-m", "Add utils"])
    run_git(tmp_path, ["add", "config.py"])
    run_git(tmp_path, ["commit", "-q", "-m", "Add config"])
    run_git(tmp_path, ["rebase", "--continue"])


def test_check_passes_after_split(tmp_path):
    level_06.setup(tmp_path)
    split(tmp_path)
    ok, message = level_06.check(tmp_path)
    assert ok


def test_check_fails_if_order_swapped(tmp_path):
    level_06.setup(tmp_path)
    run_git(
        tmp_path,
        ["-c", "sequence.editor=sed -i s/^pick/edit/", "rebase", "-i", "HEAD~1"],
    )
    run_git(tmp_path, ["reset", "HEAD^"])
    run_git(tmp_path, ["add", "config.py"])
    run_git(tmp_path, ["commit", "-q", "-m", "Add config"])
    run_git(tmp_path, ["add", "utils.py"])
    run_git(tmp_path, ["commit", "-q", "-m", "Add utils"])
    run_git(tmp_path, ["rebase", "--continue"])
    ok, message = level_06.check(tmp_path)
    assert not ok
