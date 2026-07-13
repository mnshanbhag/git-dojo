from gitdojo.levels import level_04
from gitdojo.sandbox import run_git


def test_check_fails_before_fix(tmp_path):
    level_04.setup(tmp_path)
    ok, message = level_04.check(tmp_path)
    assert not ok


def solve(tmp_path):
    (tmp_path / "app.py").write_text(level_04.FIXED)
    run_git(tmp_path, ["add", "."])
    run_git(tmp_path, ["commit", "--fixup", "HEAD", "-q"])
    run_git(
        tmp_path,
        ["-c", "sequence.editor=true", "rebase", "-i", "--autosquash", "--root"],
    )


def test_check_passes_after_fixup_autosquash(tmp_path):
    level_04.setup(tmp_path)
    solve(tmp_path)
    ok, message = level_04.check(tmp_path)
    assert ok


def test_check_fails_if_fixup_left_unsquashed(tmp_path):
    level_04.setup(tmp_path)
    (tmp_path / "app.py").write_text(level_04.FIXED)
    run_git(tmp_path, ["add", "."])
    run_git(tmp_path, ["commit", "--fixup", "HEAD", "-q"])
    ok, message = level_04.check(tmp_path)
    assert not ok
