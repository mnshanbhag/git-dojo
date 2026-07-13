import random

from gitdojo.cli import load_quotes, pick_quote


def test_load_quotes_nonempty():
    quotes = load_quotes()
    assert len(quotes) > 0
    assert all(isinstance(q, str) for q in quotes)


def test_pick_quote_is_deterministic_with_seed():
    quotes = ["a", "b", "c"]
    rng = random.Random(42)
    assert pick_quote(quotes, rng) in quotes
