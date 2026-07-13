from gitdojo.levels import level_19
from gitdojo.sandbox import run_git


def test_check_fails_before_includeif(tmp_path):
    level_19.setup(tmp_path)
    ok, message = level_19.check(tmp_path)
    assert not ok


def test_check_passes_after_includeif_configured(tmp_path):
    level_19.setup(tmp_path)
    client_a = tmp_path / "client-a"
    fake_home = tmp_path.parent / "fake-home"

    client_a_path = run_git(client_a, ["rev-parse", "--show-toplevel"]).stdout.strip()
    fake_home_config = fake_home / ".gitconfig"
    with fake_home_config.open("a") as f:
        f.write(f'\n[includeIf "gitdir:{client_a_path}/"]\n')
        f.write(f"\tpath = {fake_home.as_posix()}/.gitconfig-work\n")

    ok, message = level_19.check(tmp_path)
    assert ok
