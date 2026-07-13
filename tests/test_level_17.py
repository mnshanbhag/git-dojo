from gitdojo.levels import level_17
from gitdojo.sandbox import run_git


def test_check_fails_before_lfs_tracking(tmp_path):
    level_17.setup(tmp_path)
    ok, message = level_17.check(tmp_path)
    assert not ok


def test_check_passes_after_lfs_track_and_commit(tmp_path):
    level_17.setup(tmp_path)
    run_git(tmp_path, ["lfs", "install", "--local"])
    run_git(tmp_path, ["lfs", "track", "*.bin"])
    (tmp_path / "asset.bin").write_text("some binary-ish content\n")
    run_git(tmp_path, ["add", ".gitattributes", "asset.bin"])
    run_git(tmp_path, ["commit", "-q", "-m", "Track and add binary asset via LFS"])
    ok, message = level_17.check(tmp_path)
    assert ok


def test_check_fails_if_asset_never_committed(tmp_path):
    level_17.setup(tmp_path)
    run_git(tmp_path, ["lfs", "install", "--local"])
    run_git(tmp_path, ["lfs", "track", "*.bin"])
    (tmp_path / "asset.bin").write_text("some binary-ish content\n")
    run_git(tmp_path, ["add", ".gitattributes", "asset.bin"])
    ok, message = level_17.check(tmp_path)
    assert not ok
