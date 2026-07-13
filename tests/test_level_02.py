from gitdojo.levels import level_02
from gitdojo.sandbox import run_git


def test_check_fails_without_answer(tmp_path):
    level_02.setup(tmp_path)
    ok, message = level_02.check(tmp_path)
    assert not ok


def test_check_fails_with_reformat_commit_sha(tmp_path):
    level_02.setup(tmp_path)
    reformat_sha = run_git(
        tmp_path, ["log", "--format=%H", "-n", "1", "--skip=1"]
    ).stdout.strip()
    (tmp_path / "answer.txt").write_text(reformat_sha)
    ok, message = level_02.check(tmp_path)
    assert not ok


def test_check_passes_with_ignore_rev_result(tmp_path):
    level_02.setup(tmp_path)
    reformat_sha = run_git(
        tmp_path, ["log", "--format=%H", "-n", "1", "--skip=1"]
    ).stdout.strip()
    blame = run_git(
        tmp_path, ["blame", "-l", "--ignore-rev", reformat_sha, "poem.txt"]
    ).stdout
    first_line_sha = blame.splitlines()[0].split()[0].lstrip("^")
    (tmp_path / "answer.txt").write_text(first_line_sha)
    ok, message = level_02.check(tmp_path)
    assert ok
