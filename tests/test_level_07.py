from gitdojo.levels import level_07
from gitdojo.sandbox import run_git


def find_bug_sha(tmp_path):
    return run_git(
        tmp_path, ["log", "--format=%H", "--grep=^" + level_07.BUG_COMMIT_MESSAGE + "$"]
    ).stdout.strip().splitlines()[0]


def test_check_fails_without_answer(tmp_path):
    level_07.setup(tmp_path)
    ok, message = level_07.check(tmp_path)
    assert not ok


def test_check_fails_with_wrong_sha(tmp_path):
    level_07.setup(tmp_path)
    (tmp_path / "answer.txt").write_text("0" * 40)
    ok, message = level_07.check(tmp_path)
    assert not ok


def test_check_passes_with_bug_commit_sha(tmp_path):
    level_07.setup(tmp_path)
    (tmp_path / "answer.txt").write_text(find_bug_sha(tmp_path))
    ok, message = level_07.check(tmp_path)
    assert ok


def test_check_fails_if_bisect_left_in_progress(tmp_path):
    level_07.setup(tmp_path)
    (tmp_path / "answer.txt").write_text(find_bug_sha(tmp_path))
    run_git(tmp_path, ["bisect", "start"])
    run_git(tmp_path, ["bisect", "bad", "HEAD"])
    ok, message = level_07.check(tmp_path)
    assert not ok
    run_git(tmp_path, ["bisect", "reset"])
