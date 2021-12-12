from __future__ import annotations
from typing import Set


class Rule:
    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if isinstance(other, Rule):
            return (self.left == other.left) and (self.right == other.right)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.left, self.right))


class Grammar:
    _rules = set()

    def __init__(self, nonterms: Set[str], terms: Set[str]) -> Grammar:
        self._nonterms = nonterms
        self._terms = terms

    def add_rule(self, rule: Rule) -> None:
        self._rules.add(rule)

    def is_terminal(self, letter: str) -> bool:
        return letter in self._terms

    def rules(self) -> Set[Rule]:
        return self._rules

    def is_ks(self) -> bool:
        for rule in self._rules:
            if (len(rule.left) != 1) or (rule.left not in self._nonterms):
                return False
        return True
