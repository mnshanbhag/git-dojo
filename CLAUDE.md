# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An interactive trainer for advanced Git/GitHub techniques. It gives the user a goal, they run the real git command themselves in a disposable sandbox, and `gitdojo check` verifies the result. The code itself (a Python CLI) is the deliverable — there is no separate "app" being built.

## Commands

```
python -m venv .venv
.venv/Scripts/activate      # or: source .venv/bin/activate
pip install -e .
pip install pytest

pytest -q                          # full suite (~60 tests, ~2 min — many spawn real git subprocesses)
pytest tests/test_level_05.py -q   # single level's tests

gitdojo start <n>   # resets sandbox/, runs that level's setup()
gitdojo check       # runs that level's check() against sandbox/
gitdojo hint
gitdojo status
```

## Architecture

**Level module contract** (`src/gitdojo/levels/level_NN.py`): each exposes `ID`, `TITLE`, `CATEGORY`, `PROMPT`, `HINTS` (list, revealed one at a time every 3 failed attempts), `CANONICAL` (reference command, shown/logged only on success), `setup(sandbox_dir)`, and `check(sandbox_dir) -> (bool, str)`. `src/gitdojo/levels/__init__.py` auto-discovers modules via `pkgutil.iter_modules` — adding a new `level_NN.py` file is enough, no manual registration.

**Verification philosophy**: `check()` never inspects *how* the user solved it, only the resulting repo state (commit graph shape, file contents, config values, branch topology). This is why levels use structural assertions (`git merge-base --is-ancestor`, parent counts, `rev-list --count`) rather than trying to detect specific commands run.

**State**: `gitdojo` CLI (`cli.py`) tracks progress in `.gitdojo/state.json` (gitignored) — current level, attempt counts, completed levels. On success it writes `logs/level-NN-*.md` and flips the row in `README.md`'s table via `_slugify()`-based lookup — that table is treated as generated/authoritative progress state, not just documentation.

**Sandbox reset** (`sandbox.py`): `reset_sandbox()` wipes and recreates `sandbox/` before each `start`. On Windows, git sometimes marks object files read-only, so `shutil.rmtree` uses an `onexc` handler (`_force_remove_readonly`) that clears the attribute before retrying — don't remove this, plain `rmtree` will crash on Windows mid-curriculum.

**Levels needing more than a plain local repo** get a sibling directory next to `sandbox/` (created via `remove_dir()`/created fresh in that level's own `setup()`, not by the generic reset path): worktrees (12), submodule/subtree source repo (13), `includeIf` fake-HOME (19), sparse/shallow-clone source monorepo (20). Each level's `setup()` is responsible for cleaning up its own stray sibling dir before recreating it.

**Levels 23-25 are structurally different**: they run against a real, persistent, disposable GitHub repo (`mnshanbhag/git-dojo-gh-practice`) instead of a from-scratch local sandbox, since branch protection / Actions runs / releases only mean anything server-side. `check()` for these calls `run_gh()` (also in `sandbox.py`) and only ever issues read-only `gh api`/`gh run`/`gh release` GETs — it must never call anything that mutates repo settings (branch protection, collaborator access, etc.). That boundary is deliberate, not an oversight; if extending these levels, keep configuration steps something the human does themselves and verify by reading back state.

**Windows encoding**: any file write containing non-ASCII (the ✅/⬜ status glyphs) must pass `encoding="utf-8"` explicitly — the platform default (cp1252) will throw on emoji otherwise. See the README-rewriting code in `cli.py` for the pattern.
