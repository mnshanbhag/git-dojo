from gitdojo.levels import level_08
from gitdojo.sandbox import run_git


def test_check_fails_before_recovery(tmp_path):
    level_08.setup(tmp_path)
    ok, message = level_08.check(tmp_path)
    assert not ok


def test_check_passes_after_reflog_recovery(tmp_path):
    level_08.setup(tmp_path)
    reflog = run_git(tmp_path, ["reflog", "--format=%H %gs"]).stdout.strip().splitlines()
    lost_sha = reflog[1].split()[0]
    run_git(tmp_path, ["reset", "-q", "--hard", lost_sha])
    ok, message = level_08.check(tmp_path)
    assert ok
