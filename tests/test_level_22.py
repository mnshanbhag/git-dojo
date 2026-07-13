from gitdojo.levels import level_22
from gitdojo.sandbox import run_git


def test_check_fails_before_bundle_and_archive(tmp_path):
    level_22.setup(tmp_path)
    ok, message = level_22.check(tmp_path)
    assert not ok


def test_check_passes_after_bundle_and_archive(tmp_path):
    level_22.setup(tmp_path)
    run_git(tmp_path, ["bundle", "create", "repo.bundle", "--all"])
    run_git(tmp_path, ["archive", "--format=tar", "-o", "release.tar", "HEAD"])
    ok, message = level_22.check(tmp_path)
    assert ok


def test_check_fails_with_invalid_bundle(tmp_path):
    level_22.setup(tmp_path)
    (tmp_path / "repo.bundle").write_text("not a real bundle")
    (tmp_path / "release.tar").write_bytes(b"")
    ok, message = level_22.check(tmp_path)
    assert not ok
