"""Local, gitignored progress state for the trainer (current level, attempt
counts, completed levels)."""

import json
from dataclasses import dataclass, field
from pathlib import Path

STATE_DIRNAME = ".gitdojo"
STATE_FILENAME = "state.json"


@dataclass
class State:
    current_level: int | None = None
    attempts: dict[str, int] = field(default_factory=dict)
    completed: list[int] = field(default_factory=list)

    def attempts_for(self, level_id: int) -> int:
        return self.attempts.get(str(level_id), 0)

    def record_attempt(self, level_id: int) -> int:
        key = str(level_id)
        self.attempts[key] = self.attempts.get(key, 0) + 1
        return self.attempts[key]

    def mark_completed(self, level_id: int) -> None:
        if level_id not in self.completed:
            self.completed.append(level_id)
            self.completed.sort()
        self.attempts[str(level_id)] = 0


def _state_file(root: Path) -> Path:
    return root / STATE_DIRNAME / STATE_FILENAME


def load(root: Path) -> State:
    path = _state_file(root)
    if not path.exists():
        return State()
    data = json.loads(path.read_text())
    return State(
        current_level=data.get("current_level"),
        attempts=data.get("attempts", {}),
        completed=data.get("completed", []),
    )


def save(root: Path, state: State) -> None:
    path = _state_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "current_level": state.current_level,
                "attempts": state.attempts,
                "completed": state.completed,
            },
            indent=2,
        )
    )
