from gitdojo.levels import level_20
from gitdojo.sandbox import run_git


def solve(tmp_path):
    src_dir = tmp_path.parent / level_20.SRC_DIRNAME
    url = f"file:///{src_dir.as_posix()}"
    run_git(tmp_path, ["clone", "--depth", "1", "--no-checkout", url, "."])
    run_git(tmp_path, ["sparse-checkout", "init", "--cone"])
    run_git(tmp_path, ["sparse-checkout", "set", "services/api"])
    run_git(tmp_path, ["checkout", "-q", "main"])


def test_check_fails_before_clone(tmp_path):
    level_20.setup(tmp_path)
    ok, message = level_20.check(tmp_path)
    assert not ok


def test_check_passes_after_shallow_sparse_clone(tmp_path):
    level_20.setup(tmp_path)
    solve(tmp_path)
    ok, message = level_20.check(tmp_path)
    assert ok
    assert not (tmp_path / "services" / "web").exists()
    assert not (tmp_path / "docs").exists()


def test_check_fails_if_not_shallow(tmp_path):
    level_20.setup(tmp_path)
    src_dir = tmp_path.parent / level_20.SRC_DIRNAME
    url = f"file:///{src_dir.as_posix()}"
    run_git(tmp_path, ["clone", "--no-checkout", url, "."])
    run_git(tmp_path, ["sparse-checkout", "init", "--cone"])
    run_git(tmp_path, ["sparse-checkout", "set", "services/api"])
    run_git(tmp_path, ["checkout", "-q", "main"])
    ok, message = level_20.check(tmp_path)
    assert not ok
