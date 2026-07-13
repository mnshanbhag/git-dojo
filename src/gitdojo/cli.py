import json
import random
from importlib import resources


def load_quotes() -> list[str]:
    data = resources.files("gitdojo").joinpath("quotes.json").read_text()
    return json.loads(data)


def pick_quote(quotes: list[str], rng: random.Random | None = None) -> str:
    rng = rng or random
    return rng.choice(quotes)


def main() -> None:
    print(pick_quote(load_quotes()))


if __name__ == "__main__":
    main()
