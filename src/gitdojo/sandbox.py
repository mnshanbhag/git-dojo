"""Helpers for locating the project root and running git inside the sandbox."""

import os
import shutil
import stat
import subprocess
from pathlib import Path

ROOT_MARKER = ".gitdojo-root"
SANDBOX_DIRNAME = "sandbox"


def find_project_root(start: Path | None = None) -> Path:
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / ROOT_MARKER).exists():
            return candidate
    raise SystemExit(
        "Couldn't find a git-dojo project root (no .gitdojo-root marker in "
        "any parent directory). Run gitdojo commands from inside the "
        "git-dojo project."
    )


def sandbox_path(root: Path) -> Path:
    return root / SANDBOX_DIRNAME


def _force_remove_readonly(func, path, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def reset_sandbox(root: Path) -> Path:
    path = sandbox_path(root)
    if path.exists():
        shutil.rmtree(path, onexc=_force_remove_readonly)
    path.mkdir(parents=True)
    return path


def run_git(cwd: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )
