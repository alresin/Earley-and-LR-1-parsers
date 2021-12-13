from __future__ import annotations
from typing import Set


class Rule:
    def __init__(self, left: str, right: str) -> Rule:
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left}->{self.right})'

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Rule) -> bool:
        if isinstance(other, Rule):
            return (self.left == other.left) and (self.right == other.right)
        return False

    def __ne__(self, other: Rule) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.left, self.right))


class Grammar:
    _rules = set()

    def __init__(self, nonterms: Set[str], terms: Set[str]) -> Grammar:
        self.nonterms = nonterms
        self.terms = terms

    def add_rule(self, rule: Rule) -> None:
        self._rules.add(rule)

    def is_terminal(self, letter: str) -> bool:
        return letter in self.terms

    def rules(self) -> Set[Rule]:
        return self._rules

    def is_ks(self) -> bool:
        for rule in self._rules:
            if (len(rule.left) != 1) or (rule.left not in self.nonterms):
                return False
        return True
