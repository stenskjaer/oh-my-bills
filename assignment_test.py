import assignment


def test_normalize():
    want = " abc "
    assert assignment.normalize("abc") == want
    assert assignment.normalize("   abc  ") == want
    assert assignment.normalize("\nabc\t") == want
    assert assignment.normalize("abc[]{}") == want
    assert assignment.normalize("a|b.c.,") == want
    assert assignment.normalize("'abc'") == want
    assert assignment.normalize("abc") == want
    assert assignment.normalize("  AB.-|c[]{}\t\n") == want
