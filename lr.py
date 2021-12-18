from __future__ import annotations
from copy import deepcopy as copy
from typing import Set

from utils import Rule, Grammar
from checker import check


REAL_START = '#'
END_SYMBOL = '$'


class LR:
    def __init__(self) -> LR:
        self.grammar = None
        self.nodes = None
        self.table = None

    class Configuration:
        def __init__(self, rule: Rule, next_symbol: str, point_position: int) -> Configuration:
            self.rule = rule
            self.next_symbol = next_symbol
            self.point_position = point_position

        def __eq__(self, other: Configuration) -> bool:
            if isinstance(other, type(self)):
                return ((self.rule == other.rule) and
                        (self.next_symbol == other.next_symbol) and
                        (self.point_position == other.point_position))
            return False

        def __ne__(self, other: Configuration) -> bool:
            return not self.__eq__(other)

        def __hash__(self) -> int:
            return hash((self.rule, self.next_symbol, self.point_position))

        def __repr__(self) -> str:
            return (f'({self.rule.left}->{self.rule.right[:self.point_position]}.' +
                    '{self.rule.right[self.point_position:]}, {self.next_symbol})')

        def __str__(self) -> str:
            return self.__repr__()

    class Node:
        def __init__(self) -> Node:
            self.children = {}
            self.confs = set()

        def __repr__(self) -> str:
            return f'Node(children={str(self.children)}, confs={self.confs})'

        def __str__(self) -> str:
            return self.__repr__()

        def __eq__(self, other: Node) -> bool:
            if isinstance(other, type(self)):
                return self.confs == other.confs
            return False

        def __ne__(self, other: Node) -> bool:
            return not self.__eq__(other)

    class Shift:
        def __init__(self, to: int) -> Shift:
            self.to = to

        def __repr__(self) -> str:
            return f's{self.to}'

        def __str__(self) -> str:
            return self.__repr__()

    class Reduce:
        def __init__(self, rule: Rule) -> Reduce:
            self.rule = rule

        def __repr__(self) -> str:
            return f'r{self.rule}'

        def __str__(self) -> str:
            return self.__repr__()

    def fit(self, grammar: Grammar) -> None:
        self.grammar = grammar
        self.nodes = [self.Node()]
        self.nodes[0].confs.add(self.Configuration(Rule(REAL_START, grammar.start),
                                                   END_SYMBOL, 0))
        i = 0
        self.nodes[0] = self.closure(self.nodes[0])
        while i < len(self.nodes):
            processed = set()
            for conf in self.nodes[i].confs:
                if ((len(conf.rule.right) > conf.point_position) and
                        (conf.rule.right[conf.point_position] not in processed)):
                    self.goto(i, conf.rule.right[conf.point_position])
                    processed.add(conf.rule.right[conf.point_position])
            i += 1

        self.table = [{} for _ in range(len(self.nodes))]
        self.fill_table(0, set())

    def predict(self, word: str) -> bool:
        word += END_SYMBOL
        stack = [0]
        i = 0
        while i < len(word):
            if word[i] not in self.table[stack[-1]]:
                return False
            if isinstance(self.table[stack[-1]][word[i]], self.Reduce):
                if self.table[stack[-1]][word[i]].rule == Rule(REAL_START, self.grammar.start):
                    if i == (len(word) - 1):
                        return True
                    return False
                if (len(self.table[stack[-1]][word[i]].rule.right) * 2) >= len(stack):
                    return False
                next_stack_elem = self.table[stack[-1]][word[i]].rule.left
                stack = stack[:len(stack) - (len(self.table[stack[-1]][word[i]].rule.right) * 2)]
                stack.append(next_stack_elem)
                stack.append(self.table[stack[-2]][stack[-1]].to)

            elif isinstance(self.table[stack[-1]][word[i]], self.Shift):
                stack.append(word[i])
                stack.append(self.table[stack[-2]][word[i]].to)
                i += 1
        return False

    def closure(self, node: self.Node) -> self.Node:
        changed = True
        while changed:
            new_node = copy(node)
            changed = False
            for conf in node.confs:
                for rule in self.grammar.rules():
                    if ((len(conf.rule.right) > conf.point_position) and
                            (conf.rule.right[conf.point_position] == rule.left)):
                        for next_symbol in self.first(conf.rule.right[conf.point_position + 1:] +
                                                      conf.next_symbol, set()):
                            if self.Configuration(rule, next_symbol, 0) not in new_node.confs:
                                new_node.confs.add(self.Configuration(rule, next_symbol, 0))
                                changed = True
            node = new_node

        return node

    def goto(self, i: int, char: str) -> None:
        new_node = self.Node()
        for conf in self.nodes[i].confs:
            if ((len(conf.rule.right) > conf.point_position) and
                    (conf.rule.right[conf.point_position] == char)):
                new_node.confs.add(self.Configuration(conf.rule,
                                                      conf.next_symbol,
                                                      conf.point_position + 1))
        new_node = self.closure(new_node)
        if new_node not in self.nodes:
            self.nodes.append(new_node)
        if char in self.nodes[i].children:
            raise Exception('Not LR(1) grammar')
        self.nodes[i].children[char] = self.nodes.index(new_node)

    def fill_table(self, i: int, used: Set[int]) -> None:
        if i in used:
            return

        for symbol in self.nodes[i].children:
            self.table[i][symbol] = self.Shift(self.nodes[i].children[symbol])

        for conf in self.nodes[i].confs:
            if len(conf.rule.right) == conf.point_position:
                if conf.next_symbol in self.table[i]:
                    raise Exception('Not LR(1) grammar')
                self.table[i][conf.next_symbol] = self.Reduce(conf.rule)
        used.add(i)
        for symbol in self.nodes[i].children:
            self.fill_table(self.nodes[i].children[symbol], used)

    def first(self, w: str, current_opened) -> Set[str]:
        if w in current_opened:
            return set()
        current_opened.add(w)
        if len(w) == 0:
            return set()
        result = [w[0]]
        result_set = {w[0]}
        if self.grammar.is_terminal(w):
            return result_set
        changed = True
        while changed:
            changed = False
            u_index = 0
            while u_index < len(result):
                u = result[u_index]
                if self.grammar.is_terminal(u):
                    break
                for rule in self.grammar.rules():
                    if rule.left == u:
                        if u in result_set:
                            changed = True
                            result_set.discard(u)
                        if ((u != rule.right[:1]) and
                                (rule.right[:1] not in result_set)):
                            changed = True
                            result_set.add(rule.right[:1])
                            result.append(rule.right[:1])
                u_index += 1

        if '' in result_set:
            result_set.remove('')
            result_set.update(self.first(w[1:], current_opened))
        return result_set


if __name__ == '__main__':
    check(LR())
