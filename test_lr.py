import pytest
from utils import Rule, Grammar
from lr import LR


def test_algo_bracket_sequences_same():
    grammar = Grammar({*'S'}, {*'()'})
    for rule in {Rule('S', '(S)S'), Rule('S', '')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('')     == True
    assert algo.predict('(')    == False
    assert algo.predict(')')    == False
    assert algo.predict('()')   == True
    assert algo.predict('()()') == True
    assert algo.predict('(())') == True
    assert algo.predict('(()')  == False
    assert algo.predict(')()')  == False
    assert algo.predict(')()(') == False


def test_algo_bracket_sequences_mixed():
    grammar = Grammar({*'S'}, {*'()[]{}'})
    for rule in {Rule('S', '(S)S'), Rule('S', '[S]S'), Rule('S', '{S}S'), Rule('S', '')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('')       == True
    assert algo.predict('()')     == True
    assert algo.predict('[]{}')   == True
    assert algo.predict('[(])')   == False
    assert algo.predict('[{)]')   == False
    assert algo.predict('([]){}') == True


def test_algo_a_star():
    grammar = Grammar({*'S'}, {*'a'})
    for rule in {Rule('S', 'aS'), Rule('S', '')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('')   == True
    assert algo.predict('a')  == True
    assert algo.predict('aa') == True
    assert algo.predict('ab') == False


def test_algo_aB():
    grammar = Grammar({*'SB'}, {*'ab'})
    for rule in {Rule('S', 'aB'), Rule('B', 'b'), Rule('B','ba')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('ab')   == True
    assert algo.predict('aba')  == True
    assert algo.predict('a')    == False
    assert algo.predict('ba')   == False
    assert algo.predict('abab') == False
    assert algo.predict('abaa') == False
    assert algo.predict('ab ')  == False
    assert algo.predict('aba ') == False


def test_algo_aSbS():
    grammar = Grammar({*'S'}, {*'ab'})
    for rule in {Rule('S', 'aSbS'), Rule('S', '')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aababb')       == True
    assert algo.predict('aabbba')       == False
    assert algo.predict('ab')           == True
    assert algo.predict('abb')          == False
    assert algo.predict('abbbbb')       == False
    assert algo.predict('ba')           == False
    assert algo.predict('b')            == False
    assert algo.predict('a')            == False
    assert algo.predict('baa')          == False
    assert algo.predict('aba')          == False
    assert algo.predict('abab')         == True
    assert algo.predict('ababababab')   == True
    assert algo.predict('aaabbbababab') == True
    assert algo.predict('')             == True
    assert algo.predict(' ')            == False


def test_algo_aFb_with_G():
    grammar = Grammar({*'SFG'}, {*'ab'})
    for rule in {Rule('S', 'aFbF'), Rule('F', 'aFb'), Rule('F', ''), Rule('F', 'Ga'), Rule('G', 'bSG')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    with pytest.raises(Exception) as e:
        algo.fit(grammar)


def test_algo_aFb():
    grammar = Grammar({*'SFG'}, {*'ab'})
    for rule in {Rule('S', 'aFbF'), Rule('F', 'aFb'), Rule('F', '')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aabb')       == True
    assert algo.predict('abab')       == True
    assert algo.predict('ababab')     == False
    assert algo.predict('aabbab')     == True
    assert algo.predict('aabbaaabbb') == True
    assert algo.predict('a')          == False
    assert algo.predict('aa')         == False
    assert algo.predict('aabbb')      == False
    assert algo.predict('aabb ')      == False
    assert algo.predict('ba')         == False
    assert algo.predict('baa')        == False


def test_algo_AS():
    grammar = Grammar({*'SA'}, {*'ab'})
    for rule in {Rule('A', 'S'), Rule('S', 'aSbS'), Rule('S', '')}:
        grammar.add_rule(rule)

    grammar.start = 'A'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aababb')       == True
    assert algo.predict('aabbba')       == False
    assert algo.predict('ab')           == True
    assert algo.predict('abb')          == False
    assert algo.predict('abbbbb')       == False
    assert algo.predict('ba')           == False
    assert algo.predict('b')            == False
    assert algo.predict('a')            == False
    assert algo.predict('baa')          == False
    assert algo.predict('aba')          == False
    assert algo.predict('abab')         == True
    assert algo.predict('ababababab')   == True
    assert algo.predict('aaabbbababab') == True
    assert algo.predict('')             == True
    assert algo.predict(' ')            == False


def test_algo_aSbS_and_bSaS():
    grammar = Grammar({*'SA'}, {*'ab'})
    for rule in {Rule('A', 'S'), Rule('S', 'aSbS'), Rule('S', 'bSaS'), Rule('S', '')}:
        grammar.add_rule(rule)

    grammar.start = 'A'
    algo = LR()
    with pytest.raises(Exception) as e:
        algo.fit(grammar)


def test_algo_SaSb():
    grammar = Grammar({*'SA'}, {*'ab'})
    for rule in {Rule('S', 'SaSb'), Rule('S', '')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aabbab')       == True
    assert algo.predict('ab')           == True
    assert algo.predict('ababababab')   == True
    assert algo.predict('ababababba')   == False
    assert algo.predict('abb')          == False
    assert algo.predict('abbbbb')       == False
    assert algo.predict('ba')           == False
    assert algo.predict('b')            == False
    assert algo.predict('a')            == False
    assert algo.predict('baa')          == False
    assert algo.predict('aba')          == False
    assert algo.predict('abab')         == True
    assert algo.predict('ababababab')   == True
    assert algo.predict('aaabbbababab') == True
    assert algo.predict('')             == True
    assert algo.predict(' ')            == False
    assert algo.predict('abba')         == False
    assert algo.predict('babababa')     == False
    assert algo.predict('bababab')      == False


def test_algo_ABC():
    grammar = Grammar({*'SBC'}, {*'abc'})
    for rule in {Rule('S', 'Bb'), Rule('B', 'a'), Rule('S', 'Cc'), Rule('C', 'a')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('ab')           == True
    assert algo.predict('ac')           == True
    assert algo.predict('a')            == False
    assert algo.predict('abc')          == False
    assert algo.predict('abb')          == False
    assert algo.predict('abbbbb')       == False
    assert algo.predict('ba')           == False
    assert algo.predict('b')            == False
    assert algo.predict('a')            == False
    assert algo.predict('baa')          == False
    assert algo.predict('aba')          == False
    assert algo.predict('abab')         == False
    assert algo.predict('ababababab')   == False
    assert algo.predict('aaabbbababab') == False
    assert algo.predict('')             == False
    assert algo.predict(' ')            == False
    assert algo.predict('abba')         == False
    assert algo.predict('babababa')     == False
    assert algo.predict('bababab')      == False


def test_algo_SBC():
    grammar = Grammar({*'SBC'}, {*'abc'})
    for rule in {Rule('S', 'B'), Rule('B', 'baa'), Rule('S', ''), Rule('B', 'baaa')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('baa')          == True
    assert algo.predict('baaa')         == True
    assert algo.predict('ba')           == False
    assert algo.predict('baaaa')        == False
    assert algo.predict('abb')          == False
    assert algo.predict('abbbbb')       == False
    assert algo.predict('ba')           == False
    assert algo.predict('b')            == False
    assert algo.predict('a')            == False
    assert algo.predict('aba')          == False
    assert algo.predict('abab')         == False
    assert algo.predict('ababababab')   == False
    assert algo.predict('aaabbbababab') == False
    assert algo.predict('')             == True
    assert algo.predict(' ')            == False
    assert algo.predict('abba')         == False
    assert algo.predict('babababa')     == False
    assert algo.predict('bababab')      == False


def test_algo_BC():
    grammar = Grammar({*'SBC'}, {*'abc'})
    for rule in {Rule('S', 'B'), Rule('B', 'baa'), Rule('S', 'C'), Rule('C', 'baa')}:
        grammar.add_rule(rule)

    grammar.start = 'S'
    algo = LR()
    with pytest.raises(Exception) as e:
        algo.fit(grammar)
