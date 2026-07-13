"""Level 20 -- Sparse-checkout + shallow/partial clone."""

from pathlib import Path

from gitdojo.sandbox import remove_dir, run_git

ID = 20
TITLE = "Sparse-checkout + shallow/partial clone"
CATEGORY = "Exchange"

SRC_DIRNAME = "monorepo-src"

PROMPT = f"""\
There's a small monorepo at ../{SRC_DIRNAME} (a sibling of this sandbox)
with services/api, services/web, docs, and a root file, built up over
several commits. This sandbox itself is currently empty.

Clone it into this sandbox (`.`) as:
- a SHALLOW clone (depth 1 -- only the latest commit's history), and
- a cone-mode SPARSE-CHECKOUT limited to services/api (plus top-level
  files) -- you don't need services/web or docs checked out at all.

Note: `--depth` and `--filter` are silently ignored for a plain local
filesystem path -- you need an explicit file:// URL for them to take
effect. Get the absolute path with `cd ../{SRC_DIRNAME}` then `pwd` (or
`cd` alone on Windows), and build file:///<that path, forward slashes>.
"""

HINTS = [
    "Two separate things here: a shallow clone limits how much *history* "
    "you fetch (--depth), while sparse-checkout limits how much of the "
    "*working tree* you check out (git sparse-checkout set <paths>, after "
    "`git sparse-checkout init --cone`). Both need a real file:// URL to "
    "work against a local path.",
    f"Try: git clone --depth 1 --no-checkout "
    f"file:///<absolute-path-to-{SRC_DIRNAME}> . -- then: "
    "git sparse-checkout init --cone ; git sparse-checkout set services/api ; "
    "git checkout main",
]

CANONICAL = (
    f"git clone --depth 1 --filter=blob:none --no-checkout file:///<absolute-path-to-{SRC_DIRNAME}> .\n"
    "git sparse-checkout init --cone\n"
    "git sparse-checkout set services/api\n"
    "git checkout main"
)


def setup(sandbox_dir: Path) -> None:
    src_dir = sandbox_dir.parent / SRC_DIRNAME
    remove_dir(src_dir)
    src_dir.mkdir(parents=True)

    run_git(src_dir, ["init", "-q", "-b", "main"])
    run_git(src_dir, ["config", "user.email", "dojo@example.com"])
    run_git(src_dir, ["config", "user.name", "dojo"])

    (src_dir / "services" / "api").mkdir(parents=True)
    (src_dir / "services" / "web").mkdir(parents=True)
    (src_dir / "docs").mkdir(parents=True)
    (src_dir / "services" / "api" / "main.py").write_text("api\n")
    (src_dir / "services" / "web" / "main.py").write_text("web\n")
    (src_dir / "docs" / "README.md").write_text("readme\n")
    (src_dir / "root.txt").write_text("root\n")
    run_git(src_dir, ["add", "."])
    run_git(src_dir, ["commit", "-q", "-m", "Monorepo base"])

    (src_dir / "services" / "api" / "main.py").write_text("api v2\n")
    run_git(src_dir, ["add", "."])
    run_git(src_dir, ["commit", "-q", "-m", "Update api"])

    (src_dir / "services" / "web" / "main.py").write_text("web v2\n")
    run_git(src_dir, ["add", "."])
    run_git(src_dir, ["commit", "-q", "-m", "Update web"])


def check(sandbox_dir: Path) -> tuple[bool, str]:
    if not (sandbox_dir / ".git").exists():
        return False, "this sandbox isn't a git repo yet -- clone the monorepo into it."

    is_shallow = run_git(sandbox_dir, ["rev-parse", "--is-shallow-repository"], check=False).stdout.strip()
    if is_shallow != "true":
        return False, (
            "this isn't a shallow clone -- use --depth 1 with a file:// URL "
            "(--depth is ignored for a plain local path)."
        )

    commit_count = run_git(sandbox_dir, ["rev-list", "--count", "HEAD"]).stdout.strip()
    if commit_count != "1":
        return False, f"expected exactly 1 commit of history (depth 1), found {commit_count}."

    sparse_enabled = run_git(sandbox_dir, ["config", "core.sparseCheckout"], check=False).stdout.strip()
    if sparse_enabled != "true":
        return False, "core.sparseCheckout isn't enabled."

    if not (sandbox_dir / "services" / "api" / "main.py").exists():
        return False, "services/api/main.py should be checked out, but isn't."
    if (sandbox_dir / "services" / "web" / "main.py").exists():
        return False, "services/web/main.py shouldn't be checked out -- narrow the sparse-checkout further."
    if (sandbox_dir / "docs" / "README.md").exists():
        return False, "docs/README.md shouldn't be checked out -- narrow the sparse-checkout further."
    if not (sandbox_dir / "root.txt").exists():
        return False, "root.txt (a top-level file) should still be checked out in cone mode."

    return True, "shallow (depth 1) and sparse (cone, services/api only) clone set up correctly."
