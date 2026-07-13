"""Level registry.

Each level module exposes: ID, TITLE, CATEGORY, PROMPT, HINTS (list[str],
revealed one at a time every 3 failed attempts), CANONICAL (the reference
command(s), shown/logged only on success), setup(sandbox_dir), and
check(sandbox_dir) -> (bool, str).

Modules are discovered automatically by filename (level_NN.py) rather than
listed by hand, since this grows to 25 entries.
"""

import importlib
import pkgutil

LEVELS = {}

for _module_info in pkgutil.iter_modules(__path__):
    if not _module_info.name.startswith("level_"):
        continue
    _module = importlib.import_module(f"{__name__}.{_module_info.name}")
    LEVELS[_module.ID] = _module


def get(level_id: int):
    if level_id not in LEVELS:
        raise SystemExit(
            f"Level {level_id} isn't implemented yet. Available: "
            f"{sorted(LEVELS)}"
        )
    return LEVELS[level_id]
