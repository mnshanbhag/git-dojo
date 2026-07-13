"""Level 13 -- Submodule vs subtree."""

from pathlib import Path

from gitdojo.sandbox import remove_dir, run_git

ID = 13
TITLE = "Submodule vs subtree"
CATEGORY = "Branching"

LIB_DIRNAME = "lib-repo"

PROMPT = f"""\
There's a small library repo at ../{LIB_DIRNAME} (a sibling of this
sandbox). Pull it into this project two different ways, so you can see
how they differ under the hood:

1. Add it as a submodule at vendor/lib-submodule.
2. Add it as a subtree at vendor/lib-subtree (use --squash so its own
   history doesn't get dragged into yours).

Both end up with lib.py on disk and readable, but they're stored
completely differently: one is a pointer to a commit in another
repository, the other is fully absorbed into this repository's own tree.

(Recent git versions block submodule fetches from a plain local path by
default, as a security measure -- if `git submodule add` complains about
the "file" transport not being allowed, add `-c protocol.file.allow=always`
right after `git` on that one command.)
"""

HINTS = [
    "A submodule records a *pointer* (a gitlink, mode 160000) to a "
    "specific commit in another repo -- your repo's history never "
    "actually contains that repo's files. A subtree copies the other "
    "repo's files directly into your own tree and history, as if you'd "
    "written them yourself.",
    f"Try: git -c protocol.file.allow=always submodule add ../{LIB_DIRNAME} "
    f"vendor/lib-submodule -- then: git subtree add "
    f"--prefix=vendor/lib-subtree ../{LIB_DIRNAME} main --squash",
]

CANONICAL = (
    f"git -c protocol.file.allow=always submodule add ../{LIB_DIRNAME} vendor/lib-submodule\n"
    'git commit -m "Add submodule"        # subtree add needs a clean tree\n'
    f"git subtree add --prefix=vendor/lib-subtree ../{LIB_DIRNAME} main --squash"
)


def setup(sandbox_dir: Path) -> None:
    lib_dir = sandbox_dir.parent / LIB_DIRNAME
    remove_dir(lib_dir)
    lib_dir.mkdir(parents=True)

    run_git(lib_dir, ["init", "-q", "-b", "main"])
    run_git(lib_dir, ["config", "user.email", "dojo@example.com"])
    run_git(lib_dir, ["config", "user.name", "dojo"])
    (lib_dir / "lib.py").write_text("def util():\n    return 1\n")
    run_git(lib_dir, ["add", "."])
    run_git(lib_dir, ["commit", "-q", "-m", "Initial lib"])

    run_git(sandbox_dir, ["init", "-q", "-b", "main"])
    run_git(sandbox_dir, ["config", "user.email", "dojo@example.com"])
    run_git(sandbox_dir, ["config", "user.name", "dojo"])
    run_git(sandbox_dir, ["config", "protocol.file.allow", "always"])
    (sandbox_dir / "app.py").write_text("app = True\n")
    run_git(sandbox_dir, ["add", "."])
    run_git(sandbox_dir, ["commit", "-q", "-m", "App base"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    tree = run_git(sandbox_dir, ["ls-tree", "HEAD", "--", "vendor/"], check=False)
    if tree.returncode != 0 or not tree.stdout.strip():
        return False, "vendor/ doesn't exist in HEAD yet -- add both the submodule and the subtree first."

    entries = {}
    for line in tree.stdout.strip().splitlines():
        mode_type, _, path = line.partition("\t")
        entries[path] = mode_type.split()[0]

    if entries.get("vendor/lib-submodule") != "160000":
        return False, "vendor/lib-submodule isn't a submodule gitlink (mode 160000) -- did you use `git submodule add`?"

    if entries.get("vendor/lib-subtree") != "040000":
        return False, "vendor/lib-subtree isn't a regular tree (mode 040000) -- did you use `git subtree add`?"

    subtree_file = run_git(sandbox_dir, ["show", "HEAD:vendor/lib-subtree/lib.py"], check=False)
    if subtree_file.returncode != 0 or "return 1" not in subtree_file.stdout:
        return False, "vendor/lib-subtree/lib.py isn't inlined into this repo's history yet."

    gitmodules = sandbox_dir / ".gitmodules"
    if not gitmodules.exists() or "vendor/lib-submodule" not in gitmodules.read_text():
        return False, ".gitmodules is missing the vendor/lib-submodule entry."

    return True, "vendor/lib-submodule is a gitlink pointer; vendor/lib-subtree is fully inlined -- exactly the difference between the two."
