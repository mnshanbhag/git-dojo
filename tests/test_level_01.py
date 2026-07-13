from gitdojo.levels import level_01
from gitdojo.sandbox import run_git


def test_setup_creates_mystery_file(tmp_path):
    level_01.setup(tmp_path)
    assert (tmp_path / "mystery.txt").read_text() == level_01.MYSTERY_CONTENT


def test_check_fails_without_answer_file(tmp_path):
    level_01.setup(tmp_path)
    ok, message = level_01.check(tmp_path)
    assert not ok
    assert "answer.txt" in message


def test_check_fails_with_wrong_hash(tmp_path):
    level_01.setup(tmp_path)
    (tmp_path / "answer.txt").write_text("0" * 40)
    ok, message = level_01.check(tmp_path)
    assert not ok


def test_check_passes_with_canonical_command(tmp_path):
    level_01.setup(tmp_path)
    expected = run_git(tmp_path, ["hash-object", "mystery.txt"]).stdout.strip()
    (tmp_path / "answer.txt").write_text(expected)
    ok, message = level_01.check(tmp_path)
    assert ok
