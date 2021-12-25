from typing import Set
import pytest

from utils import Rule, Grammar


@pytest.fixture
def grammar(nonterms: Set[str], terms: Set[str], rules: Set[Rule], start: str):
    result = Grammar(nonterms, terms)
    for rule in rules:
        result.add_rule(rule)
    result.start = start
    return result
