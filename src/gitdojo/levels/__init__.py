"""Level registry.

Each level module exposes: ID, TITLE, CATEGORY, PROMPT, HINTS (list[str],
revealed one at a time every 3 failed attempts), CANONICAL (the reference
command(s), shown/logged only on success), setup(sandbox_dir), and
check(sandbox_dir) -> (bool, str).
"""

from . import (
    level_01,
    level_02,
    level_03,
    level_04,
    level_05,
    level_06,
    level_07,
    level_08,
    level_09,
    level_10,
)

LEVELS = {
    level_01.ID: level_01,
    level_02.ID: level_02,
    level_03.ID: level_03,
    level_04.ID: level_04,
    level_05.ID: level_05,
    level_06.ID: level_06,
    level_07.ID: level_07,
    level_08.ID: level_08,
    level_09.ID: level_09,
    level_10.ID: level_10,
}


def get(level_id: int):
    if level_id not in LEVELS:
        raise SystemExit(
            f"Level {level_id} isn't implemented yet. Available: "
            f"{sorted(LEVELS)}"
        )
    return LEVELS[level_id]
