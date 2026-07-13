from gitdojo.levels import level_15

HOOK_SCRIPT = (
    "#!/bin/sh\n"
    "grep -qE '^(feat|fix|chore|docs|refactor|test)(\\(.+\\))?: .+' \"$1\" || exit 1\n"
)


def test_check_fails_without_hook(tmp_path):
    level_15.setup(tmp_path)
    ok, message = level_15.check(tmp_path)
    assert not ok


def test_check_passes_with_working_hook(tmp_path):
    level_15.setup(tmp_path)
    hook_path = tmp_path / ".git" / "hooks" / "commit-msg"
    hook_path.write_text(HOOK_SCRIPT)
    hook_path.chmod(0o755)
    ok, message = level_15.check(tmp_path)
    assert ok


def test_check_fails_with_noop_hook(tmp_path):
    level_15.setup(tmp_path)
    hook_path = tmp_path / ".git" / "hooks" / "commit-msg"
    hook_path.write_text("#!/bin/sh\nexit 0\n")
    hook_path.chmod(0o755)
    ok, message = level_15.check(tmp_path)
    assert not ok
