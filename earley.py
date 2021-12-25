from __future__ import annotations
from copy import deepcopy as copy
from typing import Set, List

from utils import Rule, Grammar
from checker import check


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
        def __init__(self, rule: Rule, i: int, point_position: int, parent: Configuration) -> Configuration:
            self.rule = rule
            self.i = i
            self.point_position = point_position
            self.parent = parent

        def __repr__(self) -> str:
            return f'({self.rule.left}->{self.rule.right[:self.point_position]}.{self.rule.right[self.point_position:]}, {self.i})'

        def __str__(self) -> str:
            return self.__repr__()

        def __eq__(self, other: Configuration) -> bool:
            if isinstance(other, type(self)):
                if ((self.rule == other.rule) and (self.i == other.i) and
                    (self.point_position == other.point_position)):
                    if (self.parent == None) and (self.parent == None):
                        return True
                    return ((self.parent.rule == other.parent.rule) and
                            (self.parent.i == other.parent.i) and
                            (self.parent.point_position == other.parent.point_position))
            return False

        def __ne__(self, other: Configuration) -> bool:
            return not self.__eq__(other)

        def __hash__(self) -> int:
            if self.parent:
                return hash((self.rule, self.i, self.point_position, self.parent.rule,
                             self.parent.i, self.parent.point_position))
            return hash((self.rule, self.i, self.point_position, self.parent))

    def __init__(self) -> Earley:
        self.grammar = None

    def fit(self, grammar: Grammar) -> None:
        self.grammar = grammar

    def predict(self, word: str) -> bool:
        D = [set() for i in range(len(word) + 1)]
        D[0] = set([self.Configuration(Rule(REAL_START, self.grammar.start,), 0, 0, None)])
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

        return self.Configuration(Rule(REAL_START, self.grammar.start), 0, 1, None) in D[len(word)]

    def _scan(self, conf: self.Configuration, D: List[Set[self.Configuration]],
              j: int, letter: str) -> None:
        if ((len(conf.rule.right) > conf.point_position) and
                (conf.rule.right[conf.point_position] == letter)):
            D[j + 1].add(self.Configuration(conf.rule, conf.i, conf.point_position + 1, conf.parent))

    def _predict(self, conf: Configuration, D: List[Set[self.Configuration]],
                 j: int, current_D: List[self.Configuration]) -> List[self.Configuration]:
        for rule in self.grammar.rules():
            if ((len(conf.rule.right) > conf.point_position) and
                    (conf.rule.right[conf.point_position] == rule.left)):
                adding_conf = self.Configuration(rule, j, 0, conf)
                if adding_conf not in D[j]:
                    current_D.append(adding_conf)
                    D[j].add(adding_conf)

    def _complete(self, conf: Configuration, D: List[Set[self.Configuration]],
                  j: int, current_D: List[self.Configuration]) -> Set[self.Configuration]:
        if j != conf.i:
            for prev_conf in D[conf.i]:
                if ((len(prev_conf.rule.right) > prev_conf.point_position) and
                        (prev_conf.rule.right[prev_conf.point_position] == conf.rule.left)):
                    adding_conf = self.Configuration(prev_conf.rule, prev_conf.i,
                                                     prev_conf.point_position + 1,
                                                     prev_conf.parent)
                    if adding_conf not in D[j]:
                        current_D.append(adding_conf)
                        D[j].add(adding_conf)
        else:
            prev_conf_index = 0
            while prev_conf_index < len(current_D):
                prev_conf = current_D[prev_conf_index]
                if ((len(prev_conf.rule.right) > prev_conf.point_position) and
                        (prev_conf.rule.right[prev_conf.point_position] == conf.rule.left)):
                    adding_conf = self.Configuration(prev_conf.rule, prev_conf.i,
                                                     prev_conf.point_position + 1,
                                                     prev_conf.parent)
                    if adding_conf not in D[j]:
                        current_D.append(adding_conf)
                        D[j].add(adding_conf)
                prev_conf_index += 1


if __name__ == '__main__':
    check(Earley())
