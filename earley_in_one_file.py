from __future__ import annotations
from copy import deepcopy as copy
from typing import Set, List


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
    def __init__(self, nonterms: Set[str], terms: Set[str]) -> Grammar:
        self.nonterms = nonterms
        self.terms = terms
        self._rules = set()

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


def check(algorithm: Union[Earley, LR]) -> None:
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


REAL_START = '#'


def debug_print(D: List[Set[Configuration]]):
    for i, di in enumerate(D):
        print(f'D{i}:')
        for conf in di:
            print(conf)
        print()
    print()


class Earley:
    class Configuration:
        def __init__(self, rule: Rule, i: int, point_position: int) -> Configuration:
            self.rule = rule
            self.i = i
            self.point_position = point_position

        def __repr__(self) -> str:
            return f'({self.rule.left}->{self.rule.right[:self.point_position]}.{self.rule.right[self.point_position:]}, {self.i})'

        def __str__(self) -> str:
            return self.__repr__()

        def __eq__(self, other: Configuration) -> bool:
            if isinstance(other, type(self)):
                return ((self.rule == other.rule) and
                        (self.i == other.i) and
                        (self.point_position == other.point_position))
            return False

        def __ne__(self, other: Configuration) -> bool:
            return not self.__eq__(other)

        def __hash__(self) -> int:
            return hash((self.rule, self.i, self.point_position))

    def __init__(self) -> Earley:
        self.grammar = None

    def fit(self, grammar: Grammar) -> None:
        self.grammar = grammar

    def predict(self, word: str) -> bool:
        D = [set() for i in range(len(word) + 1)]
        D[0] = set([self.Configuration(Rule(REAL_START, self.grammar.start,), 0, 0)])
        for i in range(len(word) + 1):
            current_D = [x for x in D[i]]
            conf_index = 0
            count = 0
            while conf_index < len(current_D):
                count += 1
                conf = current_D[conf_index]
                if len(conf.rule.right) != conf.point_position:
                    if ((len(conf.rule.right) > conf.point_position) and
                            (conf.rule.right[conf.point_position] not in self.grammar.terms)):
                        self._predict(conf, D, i, current_D)
                    elif i < len(word):
                        self._scan(conf, D, i, word[i])
                else:
                    D[i] = set(current_D)
                    self._complete(conf, D, i, current_D)
                conf_index += 1

            D[i] = set(current_D)

        return self.Configuration(Rule(REAL_START, self.grammar.start), 0, 1) in D[len(word)]

    def _scan(self, conf: self.Configuration, D: List[Set[self.Configuration]],
              j: int, letter: str) -> None:
        if ((len(conf.rule.right) > conf.point_position) and
                (conf.rule.right[conf.point_position] == letter)):
            D[j + 1].add(self.Configuration(conf.rule, conf.i, conf.point_position + 1))

    def _predict(self, conf: Configuration, D: List[Set[self.Configuration]],
                 j: int, current_D: List[self.Configuration]) -> List[self.Configuration]:
        for rule in self.grammar.rules():
            if ((len(conf.rule.right) > conf.point_position) and
                    (conf.rule.right[conf.point_position] == rule.left)):
                if self.Configuration(rule, conf.i, 0) not in D[j]:
                    current_D.append(self.Configuration(rule, j, 0))
                    D[j].add(self.Configuration(rule, j, 0))

    def _complete(self, conf: Configuration, D: List[Set[self.Configuration]],
                  j: int, current_D: List[self.Configuration]) -> Set[self.Configuration]:
        if j != conf.i:
            for prev_conf in D[conf.i]:
                if ((len(prev_conf.rule.right) > prev_conf.point_position) and
                        (prev_conf.rule.right[prev_conf.point_position] == conf.rule.left)):
                    if self.Configuration(prev_conf.rule, prev_conf.i,
                                          prev_conf.point_position + 1) not in D[j]:
                        current_D.append(self.Configuration(prev_conf.rule, prev_conf.i,
                                                            prev_conf.point_position + 1))
                        D[j].add(self.Configuration(prev_conf.rule, prev_conf.i,
                                                    prev_conf.point_position + 1))
        else:
            prev_conf_index = 0
            while prev_conf_index < len(current_D):
                prev_conf = current_D[prev_conf_index]
                if ((len(prev_conf.rule.right) > prev_conf.point_position) and
                        (prev_conf.rule.right[prev_conf.point_position] == conf.rule.left)):
                    if self.Configuration(prev_conf.rule, prev_conf.i,
                                          prev_conf.point_position + 1) not in D[j]:
                        current_D.append(self.Configuration(prev_conf.rule, prev_conf.i,
                                                            prev_conf.point_position + 1))
                        D[j].add(self.Configuration(prev_conf.rule, prev_conf.i,
                                                    prev_conf.point_position + 1))
                prev_conf_index += 1


if __name__ == '__main__':
    check(Earley())
