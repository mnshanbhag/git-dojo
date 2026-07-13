from gitdojo.levels import level_03
from gitdojo.sandbox import run_git


def test_check_fails_without_note(tmp_path):
    level_03.setup(tmp_path)
    ok, message = level_03.check(tmp_path)
    assert not ok
    assert "no note" in message


def test_check_fails_with_wrong_note_text(tmp_path):
    level_03.setup(tmp_path)
    run_git(tmp_path, ["notes", "add", "-m", "wrong text", "HEAD"])
    ok, message = level_03.check(tmp_path)
    assert not ok


def test_check_passes_with_correct_note(tmp_path):
    level_03.setup(tmp_path)
    run_git(tmp_path, ["notes", "add", "-m", level_03.NOTE_TEXT, "HEAD"])
    ok, message = level_03.check(tmp_path)
    assert ok
