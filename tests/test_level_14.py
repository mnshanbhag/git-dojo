from gitdojo.levels import level_14
from gitdojo.sandbox import run_git


def test_check_fails_before_stashing(tmp_path):
    level_14.setup(tmp_path)
    ok, message = level_14.check(tmp_path)
    assert not ok


def solve(tmp_path):
    run_git(tmp_path, ["stash", "push", "-q", "-m", "urgent-fix", "--", "file_a.txt"])
    run_git(tmp_path, ["stash", "push", "-q", "-m", "wip-feature", "--", "file_b.txt"])
    stash_list = run_git(tmp_path, ["stash", "list"]).stdout.strip().splitlines()
    urgent_ref = next(
        line.split(":")[0] for line in stash_list if "urgent-fix" in line
    )
    run_git(tmp_path, ["stash", "branch", "urgent-fix-branch", urgent_ref])


def test_check_passes_after_split_stash_and_branch(tmp_path):
    level_14.setup(tmp_path)
    solve(tmp_path)
    ok, message = level_14.check(tmp_path)
    assert ok
