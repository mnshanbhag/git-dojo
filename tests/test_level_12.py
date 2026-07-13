from gitdojo.levels import level_12
from gitdojo.sandbox import run_git


def test_check_fails_before_worktree(tmp_path):
    level_12.setup(tmp_path)
    ok, message = level_12.check(tmp_path)
    assert not ok


def test_check_passes_after_worktree_add(tmp_path):
    level_12.setup(tmp_path)
    worktree_dir = tmp_path.parent / level_12.WORKTREE_DIRNAME
    run_git(tmp_path, ["worktree", "add", str(worktree_dir), "-b", "hotfix", "main"])
    (worktree_dir / "hotfix.txt").write_text("urgent fix\n")
    run_git(worktree_dir, ["add", "."])
    run_git(worktree_dir, ["commit", "-q", "-m", "Add urgent hotfix"])

    ok, message = level_12.check(tmp_path)
    assert ok

    current_branch = run_git(tmp_path, ["branch", "--show-current"]).stdout.strip()
    assert current_branch == "feature"

    run_git(tmp_path, ["worktree", "remove", str(worktree_dir), "--force"])
