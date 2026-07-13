import argparse
import datetime as dt
import re
from pathlib import Path

from gitdojo import levels, state
from gitdojo.sandbox import find_project_root, reset_sandbox, sandbox_path

ATTEMPTS_PER_HINT = 3


def cmd_start(args: argparse.Namespace) -> None:
    root = find_project_root()
    level = levels.get(args.level)

    sandbox = reset_sandbox(root)
    level.setup(sandbox)

    st = state.load(root)
    st.current_level = level.ID
    st.attempts[str(level.ID)] = 0
    state.save(root, st)

    print(f"== Level {level.ID}: {level.TITLE} ({level.CATEGORY}) ==\n")
    print(level.PROMPT)
    print(f"Sandbox ready at: {sandbox}")
    print("Do your work there, then run `gitdojo check` from anywhere in this project.")


def _current_level(root: Path):
    st = state.load(root)
    if st.current_level is None:
        raise SystemExit("No level in progress. Run `gitdojo start <n>` first.")
    return st, levels.get(st.current_level)


def cmd_check(args: argparse.Namespace) -> None:
    root = find_project_root()
    st, level = _current_level(root)
    sandbox = sandbox_path(root)

    ok, message = level.check(sandbox)

    if ok:
        st.mark_completed(level.ID)
        state.save(root, st)
        print(f"Correct! {message}\n")
        print(f"Reference command: {level.CANONICAL}")
        _log_completion(root, level)
        _update_readme(root, level)
        print("\nLogged and marked complete in README.md.")
        return

    attempts = st.record_attempt(level.ID)
    state.save(root, st)
    print(f"Not quite: {message}")

    if attempts % ATTEMPTS_PER_HINT == 0:
        hint_index = min(attempts // ATTEMPTS_PER_HINT - 1, len(level.HINTS) - 1)
        print(f"\nNudge: {level.HINTS[hint_index]}")
    else:
        remaining = ATTEMPTS_PER_HINT - (attempts % ATTEMPTS_PER_HINT)
        print(f"({remaining} more attempt(s) before the next nudge -- attempt {attempts} so far)")


def cmd_hint(args: argparse.Namespace) -> None:
    root = find_project_root()
    st, level = _current_level(root)
    attempts = max(st.attempts_for(level.ID), ATTEMPTS_PER_HINT)
    hint_index = min(attempts // ATTEMPTS_PER_HINT - 1, len(level.HINTS) - 1)
    print(level.HINTS[hint_index])


def cmd_status(args: argparse.Namespace) -> None:
    root = find_project_root()
    st = state.load(root)
    print(f"Current level: {st.current_level}")
    print(f"Completed: {sorted(st.completed) or 'none yet'}")
    for level_id in sorted(levels.LEVELS):
        mark = "done" if level_id in st.completed else f"{st.attempts_for(level_id)} attempt(s)"
        print(f"  Level {level_id}: {levels.LEVELS[level_id].TITLE} -- {mark}")


def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower())
    return slug.strip("-")


def _log_completion(root: Path, level) -> None:
    logs_dir = root / "logs"
    logs_dir.mkdir(exist_ok=True)
    slug = _slugify(level.TITLE)
    log_file = logs_dir / f"level-{level.ID:02d}-{slug}.md"
    log_file.write_text(
        f"# Level {level.ID} -- {level.TITLE}\n\n"
        f"Category: {level.CATEGORY}\n"
        f"Completed: {dt.date.today().isoformat()}\n\n"
        f"## Goal\n\n{level.PROMPT}\n"
        f"## Reference command\n\n```\n{level.CANONICAL}\n```\n",
        encoding="utf-8",
    )


def _update_readme(root: Path, level) -> None:
    readme = root / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    lines = text.splitlines()
    prefix = f"| {level.ID} |"
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            cells = line.split("|")
            # cells: ['', ' 1 ', ' Title ', ' Category ', ' Status ', ' Log ', '']
            cells[4] = " ✅ "
            slug = _slugify(level.TITLE)
            cells[5] = f" [log](logs/level-{level.ID:02d}-{slug}.md) "
            lines[i] = "|".join(cells)
            break
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(prog="gitdojo")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Set up the sandbox for a level")
    p_start.add_argument("level", type=int)
    p_start.set_defaults(func=cmd_start)

    p_check = sub.add_parser("check", help="Check the sandbox against the current level's goal")
    p_check.set_defaults(func=cmd_check)

    p_hint = sub.add_parser("hint", help="Show the current hint on demand")
    p_hint.set_defaults(func=cmd_hint)

    p_status = sub.add_parser("status", help="Show progress across levels")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
