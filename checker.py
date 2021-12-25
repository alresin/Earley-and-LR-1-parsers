from __future__ import annotations
from typing import Union

from utils import Rule, Grammar


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

    if not grammar.is_context_free():
        raise Exception('Wrong grammar')

    algorithm.fit(grammar)

    words_count = int(input())
    for _ in range(words_count):
        word = input()
        for letter in word:
            if not grammar.is_terminal(letter):
                raise Exception('Wrong word')
        print('Yes' if algorithm.predict(word) else 'No')
