"""Level 19 -- Conditional config: includeIf."""

import os
from pathlib import Path

from gitdojo.sandbox import remove_dir, run_git

ID = 19
TITLE = "Conditional config: includeIf"
CATEGORY = "Config"

PROMPT = """\
There's a fake HOME directory at ../fake-home (a sibling of this
sandbox) -- we use a fake one so this exercise never touches your real
~/.gitconfig. It has a base .gitconfig (default email:
dojo-personal@example.com) and a .gitconfig-work file (email:
dojo-work@example.com) ready to be pulled in conditionally.

This sandbox has two nested repos: client-a/ and personal/. Add an
includeIf directive to ../fake-home/.gitconfig so that ONLY repos under
client-a/ pick up .gitconfig-work's email -- personal/ should keep the
default.

To test without touching your real home config, run git with HOME
pointed at the fake one, e.g. (adjust the path to your actual sandbox):
  HOME=<absolute path to ../fake-home> git -C client-a config user.email
  HOME=<absolute path to ../fake-home> git -C personal config user.email
The first should print dojo-work@example.com, the second
dojo-personal@example.com.
"""

HINTS = [
    "includeIf conditionally pulls in another config file based on where "
    "the CURRENT repository's .git directory lives. The condition is a "
    "section header in the including file: "
    '[includeIf "gitdir:<absolute-path>/"], with path = <file-to-include> '
    "underneath. A trailing slash on the gitdir pattern matches that "
    "whole directory tree.",
    "Get client-a's absolute path with `git -C client-a rev-parse "
    "--show-toplevel`, add that (with a trailing slash) as a gitdir "
    "pattern in ../fake-home/.gitconfig pointing to "
    "../fake-home/.gitconfig-work, then test with the HOME-override "
    "commands above.",
]

CANONICAL = (
    "git -C client-a rev-parse --show-toplevel     # get client-a's absolute path\n"
    "# add to ../fake-home/.gitconfig:\n"
    '#   [includeIf "gitdir:<that-path>/"]\n'
    "#       path = <absolute-path-to-fake-home>/.gitconfig-work\n"
    "HOME=<absolute-path-to-fake-home> git -C client-a config user.email"
)


def setup(sandbox_dir: Path) -> None:
    fake_home = sandbox_dir.parent / "fake-home"
    remove_dir(fake_home)
    fake_home.mkdir(parents=True)

    (fake_home / ".gitconfig").write_text(
        "[user]\n\tname = dojo\n\temail = dojo-personal@example.com\n"
    )
    (fake_home / ".gitconfig-work").write_text(
        "[user]\n\temail = dojo-work@example.com\n"
    )

    client_a = sandbox_dir / "client-a"
    personal = sandbox_dir / "personal"
    client_a.mkdir()
    personal.mkdir()
    run_git(client_a, ["init", "-q", "-b", "main"])
    run_git(personal, ["init", "-q", "-b", "main"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    fake_home = sandbox_dir.parent / "fake-home"
    if not (fake_home / ".gitconfig").exists():
        return False, "../fake-home/.gitconfig is missing."

    client_a = sandbox_dir / "client-a"
    personal = sandbox_dir / "personal"

    env = {**os.environ, "HOME": str(fake_home)}

    work_email = run_git(client_a, ["config", "user.email"], check=False, env=env).stdout.strip()
    if work_email != "dojo-work@example.com":
        return False, (
            f"client-a's effective user.email is '{work_email}', expected "
            "'dojo-work@example.com' -- check your includeIf gitdir pattern."
        )

    personal_email = run_git(personal, ["config", "user.email"], check=False, env=env).stdout.strip()
    if personal_email != "dojo-personal@example.com":
        return False, (
            f"personal's effective user.email is '{personal_email}', expected "
            "'dojo-personal@example.com' -- the includeIf shouldn't affect "
            "repos outside client-a."
        )

    return True, "client-a picks up the work email via includeIf; personal keeps the default."
