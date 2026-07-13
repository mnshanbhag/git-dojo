from gitdojo.levels import level_21
from gitdojo.sandbox import run_git


def test_check_fails_before_patches(tmp_path):
    level_21.setup(tmp_path)
    ok, message = level_21.check(tmp_path)
    assert not ok


def test_check_passes_after_format_patch_and_am(tmp_path):
    level_21.setup(tmp_path)
    (tmp_path / "patches").mkdir()
    run_git(tmp_path, ["format-patch", "main..feature", "-o", "patches"])
    run_git(tmp_path, ["checkout", "-q", "target"])
    patch_files = sorted((tmp_path / "patches").glob("*.patch"))
    run_git(tmp_path, ["am", *[str(p) for p in patch_files]])
    ok, message = level_21.check(tmp_path)
    assert ok
