from __future__ import annotations
from copy import deepcopy as copy
from typing import Set, List


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


def check(algorithm: Earley) -> None:
    try:
        nonterm_count, term_count, rules_count = [int(x) for x in input().split()]
        nonterms = {x for x in input()}
        terms = {x for x in input()}
        grammar = Grammar(nonterms, terms)
    except:
        raise Exception('Wrong input format')
    for _ in range(rules_count):
        row = input()
        for letter in row:
            if ((letter not in set(['-', '>'])) and
                    (letter not in nonterms) and
                    (letter not in terms)):
                raise Exception('Wrong input format')
        grammar.add_rule(Rule(*row.split('->')))
    try:
        grammar.start = input()
    except:
        raise Exception('Wrong input format')

    if grammar.start not in nonterms:
        raise Exception('Start symbol is not a nonterminal')

    if not grammar.is_ks():
        raise Exception('Wrong grammar')

    algorithm.fit(grammar)

    words_count = int(input())
    for _ in range(words_count):
        word = input()
        for letter in word:
            if not grammar.is_terminal(letter):
                raise Exception('Wrong word')
        print('Yes' if algorithm.predict(word) else 'No')


class Earley:
    class Configuration:
        def __init__(self, rule: Rule, i: int, point_position: int) -> Configuration:
            self.rule = rule
            self.i = i
            self.point_position = point_position

        def __repr__(self):
            return f'({self.rule.left}->{self.rule.right[:self.point_position]}.{self.rule.right[self.point_position:]}, {self.i})'

        def __str__(self):
            return self.__repr__()

        def __eq__(self, other):
            if isinstance(other, type(self)):
                return ((self.rule == other.rule) and
                        (self.i == other.i) and
                        (self.point_position == other.point_position))
            return False

        def __ne__(self, other):
            return not self.__eq__(other)

        def __hash__(self):
            return hash((self.rule, self.i, self.point_position))

    def __init__(self) -> Earley:
        self.grammar = None

    def fit(self, grammar: Grammar) -> None:
        self.grammar = grammar

    def predict(self, word: str) -> bool:
        D = [set() for i in range(len(word) + 1)]
        D[0] = set([self.Configuration(Rule('#', self.grammar.start,), 0, 0)])
        while True:
            new_dj = self._complete(D, 0)
            not_changed = (new_dj == D[0])
            D[0] = new_dj
            new_dj = self._predict(D, 0)
            not_changed = (new_dj == D[0])
            D[0] = new_dj
            if not_changed:
                break

        for index, letter in enumerate(word):
            self._scan(D, index, letter)
            while True:
                new_dj = self._complete(D, index + 1)
                not_changed = (new_dj == D[index + 1])
                D[index + 1] = new_dj
                new_dj = self._predict(D, index + 1)
                not_changed = not_changed and (new_dj == D[index + 1])
                D[index + 1] = new_dj
                if not_changed:
                    break

        return self.Configuration(Rule('#', self.grammar.start), 0, 1) in D[len(word)]


    def _scan(self, D: List[Set[self.Configuration]], j: int, letter: str) -> None:
        for conf in D[j]:
            if ((len(conf.rule.right) > conf.point_position) and
                    (self.grammar.is_terminal(conf.rule.right[conf.point_position])) and
                    (conf.rule.right[conf.point_position] == letter)):
                D[j + 1].add(self.Configuration(conf.rule, conf.i, conf.point_position + 1))

    def _predict(self, D: List[Set[self.Configuration]], j: int) -> Set[self.Configuration]:
        new_dj = copy(D[j])
        for conf in D[j]:
            for rule in self.grammar.rules():
                if ((len(conf.rule.right) > conf.point_position) and
                        (rule.left == conf.rule.right[conf.point_position])):
                    new_dj.add(self.Configuration(rule, j, 0))
        return new_dj

    def _complete(self, D: List[Set[self.Configuration]], j: int) -> Set[self.Configuration]:
        new_dj = copy(D[j])
        for conf in D[j]:
            if conf.point_position == len(conf.rule.right):
                for prev_conf in D[conf.i]:
                    if ((len(prev_conf.rule.right) > prev_conf.point_position) and
                            (conf.rule.left == prev_conf.rule.right[prev_conf.point_position])):
                        new_dj.add(self.Configuration(prev_conf.rule,
                                                      prev_conf.i,
                                                      prev_conf.point_position + 1))
        return new_dj


if __name__ == '__main__':
    check(Earley())
