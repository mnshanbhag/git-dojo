"""Level registry.

Each level module exposes: ID, TITLE, CATEGORY, PROMPT, HINTS (list[str],
revealed one at a time every 3 failed attempts), CANONICAL (the reference
command(s), shown/logged only on success), setup(sandbox_dir), and
check(sandbox_dir) -> (bool, str).
"""

from . import level_01

LEVELS = {
    level_01.ID: level_01,
}


def get(level_id: int):
    if level_id not in LEVELS:
        raise SystemExit(
            f"Level {level_id} isn't implemented yet. Available: "
            f"{sorted(LEVELS)}"
        )
    return LEVELS[level_id]
