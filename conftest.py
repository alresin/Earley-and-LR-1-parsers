from typing import Set
import pytest

from utils import Rule, Grammar


def fixture(nonterms: Set[str], terms: Set[str], rules: Set[Rule], start: str):
    def wrapper(func):
        def wrap(*args, **kwargs):
            grammar = Grammar(nonterms, terms)
            for rule in rules:
                grammar.add_rule(rule)
            grammar.start = start
            return func(grammar)
        return wrap
    return wrapper

