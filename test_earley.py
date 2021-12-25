import pytest

from conftest import grammar
from utils import Rule, Grammar
from earley import Earley


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'()'}])
@pytest.mark.parametrize('rules', [{Rule('S', '(S)S'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_bracket_sequences_same(grammar):
    algo = Earley()
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


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'()[]{}'}])
@pytest.mark.parametrize('rules', [{Rule('S', '(S)S'), Rule('S', '[S]S'), Rule('S', '{S}S'),
                                    Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_bracket_sequences_mixed(grammar):
    algo = Earley()
    algo.fit(grammar)
    assert algo.predict('')       == True
    assert algo.predict('()')     == True
    assert algo.predict('[]{}')   == True
    assert algo.predict('[(])')   == False
    assert algo.predict('[{)]')   == False
    assert algo.predict('([]){}') == True


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'a'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'aS'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_a_star(grammar):
    algo = Earley()
    algo.fit(grammar)
    assert algo.predict('')   == True
    assert algo.predict('a')  == True
    assert algo.predict('aa') == True
    assert algo.predict('ab') == False



@pytest.mark.parametrize('nonterms', [{*'SB'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'aB'), Rule('B', 'b'), Rule('B','ba')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aB(grammar):
    algo = Earley()
    algo.fit(grammar)
    assert algo.predict('ab')   == True
    assert algo.predict('aba')  == True
    assert algo.predict('a')    == False
    assert algo.predict('ba')   == False
    assert algo.predict('abab') == False
    assert algo.predict('abaa') == False
    assert algo.predict('ab ')  == False
    assert algo.predict('aba ') == False


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'aSbS'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aSbS(grammar):
    algo = Earley()
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


@pytest.mark.parametrize('nonterms', [{*'SFG'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'aFbF'), Rule('F', 'aFb'), Rule('F', ''),
                                    Rule('F', 'Ga'), Rule('G', 'bSG')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aFb_with_G(grammar):
    algo = Earley()
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


@pytest.mark.parametrize('nonterms', [{*'SFG'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'aFbF'), Rule('F', 'aFb'), Rule('F', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aFb(grammar):
    algo = Earley()
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


@pytest.mark.parametrize('nonterms', [{*'SA'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('A', 'S'), Rule('S', 'aSbS'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'A')
def test_algo_AS(grammar):
    algo = Earley()
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

@pytest.mark.parametrize('nonterms', [{*'SA'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('A', 'S'), Rule('S', 'aSbS'), Rule('S', 'bSaS'),
                                    Rule('S', '')}])
@pytest.mark.parametrize('start', 'A')
def test_algo_aSbS_and_bSaS(grammar):
    algo = Earley()
    algo.fit(grammar)
    assert algo.predict('aababb')       == True
    assert algo.predict('aabbba')       == True
    assert algo.predict('ababba')       == True
    assert algo.predict('ab')           == True
    assert algo.predict('abb')          == False
    assert algo.predict('abbbbb')       == False
    assert algo.predict('ba')           == True
    assert algo.predict('b')            == False
    assert algo.predict('a')            == False
    assert algo.predict('baa')          == False
    assert algo.predict('aba')          == False
    assert algo.predict('abab')         == True
    assert algo.predict('ababababab')   == True
    assert algo.predict('aaabbbababab') == True
    assert algo.predict('')             == True
    assert algo.predict(' ')            == False
    assert algo.predict('abba')         == True
    assert algo.predict('babababa')     == True
    assert algo.predict('bababab')      == False

@pytest.mark.parametrize('nonterms', [{*'SA'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'SaSb'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SaSb(grammar):
    algo = Earley()
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


@pytest.mark.parametrize('nonterms', [{*'SBC'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'Bb'), Rule('B', 'a'), Rule('S', 'Cc'),
                                    Rule('C', 'a')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_ABC(grammar):
    algo = Earley()
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
    # assert algo.predict('ababababab')   == False
    # assert algo.predict('aaabbbababab') == False
    assert algo.predict('')             == False
    assert algo.predict(' ')            == False
    assert algo.predict('abba')         == False
    assert algo.predict('babababa')     == False
    assert algo.predict('bababab')      == False


@pytest.mark.parametrize('nonterms', [{*'SBC'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'B'), Rule('B', 'baa'), Rule('S', ''),
                                    Rule('B', 'baaa')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SBC(grammar):
    algo = Earley()
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
    # assert algo.predict('ababababab')   == False
    # assert algo.predict('aaabbbababab') == False
    assert algo.predict('')             == True
    assert algo.predict(' ')            == False
    assert algo.predict('abba')         == False
    assert algo.predict('babababa')     == False
    assert algo.predict('bababab')      == False


@pytest.mark.parametrize('nonterms', [{*'SBC'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'B'), Rule('B', 'baa'), Rule('S', 'C'),
                                    Rule('C', 'baa')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_BC(grammar):
    algo = Earley()
    algo.fit(grammar)
    assert algo.predict('baa')          == True
    assert algo.predict('baaa')         == False
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
    assert algo.predict('')             == False
    assert algo.predict(' ')            == False
    assert algo.predict('abba')         == False
    assert algo.predict('babababa')     == False
    assert algo.predict('bababab')      == False


@pytest.mark.parametrize('nonterms', [{*'SAB'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'SABSBASABAABSSSAabc'), Rule('S', ''),
                                    Rule('A', ''), Rule('B', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SABS(grammar):
    algo = Earley()
    algo.fit(grammar)
    assert algo.predict('abc')       == True
    assert algo.predict('a')         == False
    assert algo.predict('b')         == False
    assert algo.predict('c')         == False
    assert algo.predict('bc')        == False
    assert algo.predict('ab')        == False
    assert algo.predict('ac')        == False
    assert algo.predict('abcabc')    == True
    assert algo.predict('abcabcabc') == True
    assert algo.predict('abcab')     == False
    assert algo.predict('')          == True


@pytest.mark.parametrize('nonterms', [{*'SAB'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'SABBAabc'), Rule('S', ''), Rule('A', ''),
                                    Rule('B', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SAB(grammar):
    algo = Earley()
    algo.fit(grammar)
    assert algo.predict('abc')       == True
    assert algo.predict('a')         == False
    assert algo.predict('b')         == False
    assert algo.predict('c')         == False
    assert algo.predict('bc')        == False
    assert algo.predict('ab')        == False
    assert algo.predict('ac')        == False
    assert algo.predict('abcabc')    == True
    assert algo.predict('abcabcabc') == True
    assert algo.predict('abcab')     == False
    assert algo.predict('')          == True
