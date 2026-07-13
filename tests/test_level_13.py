from gitdojo.levels import level_13
from gitdojo.sandbox import run_git


def test_check_fails_before_add(tmp_path):
    level_13.setup(tmp_path)
    ok, message = level_13.check(tmp_path)
    assert not ok


def test_check_passes_after_submodule_and_subtree_add(tmp_path):
    level_13.setup(tmp_path)
    lib_dir = tmp_path.parent / level_13.LIB_DIRNAME

    run_git(
        tmp_path,
        ["-c", "protocol.file.allow=always", "submodule", "add", str(lib_dir), "vendor/lib-submodule"],
    )
    run_git(tmp_path, ["commit", "-q", "-m", "Add submodule"])
    run_git(
        tmp_path,
        [
            "subtree", "add", "--prefix=vendor/lib-subtree",
            str(lib_dir), "main", "--squash",
        ],
    )

    ok, message = level_13.check(tmp_path)
    assert ok
