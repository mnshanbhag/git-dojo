from gitdojo.levels import level_16
from gitdojo.sandbox import run_git


def test_check_fails_without_union_driver(tmp_path):
    level_16.setup(tmp_path)
    ok, message = level_16.check(tmp_path)
    assert not ok


def test_check_passes_with_union_merge(tmp_path):
    level_16.setup(tmp_path)
    (tmp_path / ".gitattributes").write_text("CHANGELOG.txt merge=union\n")
    run_git(tmp_path, ["add", ".gitattributes"])
    run_git(tmp_path, ["commit", "-q", "-m", "Add union merge driver"])
    run_git(tmp_path, ["merge", "feature", "-q", "-m", "Merge feature"])
    ok, message = level_16.check(tmp_path)
    assert ok
    assert "<<<<<<<" not in (tmp_path / "CHANGELOG.txt").read_text()


def test_check_fails_if_merge_conflicts_left_unresolved(tmp_path):
    level_16.setup(tmp_path)
    result = run_git(tmp_path, ["merge", "feature", "-q", "-m", "Merge feature"], check=False)
    assert result.returncode != 0
    ok, message = level_16.check(tmp_path)
    assert not ok
