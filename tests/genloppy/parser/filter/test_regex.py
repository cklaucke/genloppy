import pytest

from genloppy.parser.filter.regex import RegexFilter


def test_01_valid_regular_expressions():
    """Tests that valid regular expressions do not raise.

    tests: R-PARSER-FILTER-REGEX-001
    tests: R-PARSER-FILTER-REGEX-002
    """
    regexes = ["foo",
               "foo.*",
               "(foo|bar)"]
    RegexFilter(regexes)


def test_02_invalid_regular_expressions():
    """Tests that invalid regular expressions raise.

    tests: R-PARSER-FILTER-REGEX-001
    tests: R-PARSER-FILTER-REGEX-002
    """
    regexes = ["(foo|bar"]
    with pytest.raises(RuntimeError) as cm:
        RegexFilter(regexes)

    assert cm.match("Malformed regular expressions given")
    message = str(cm.value)
    for regex in regexes:
        assert message.find(regex)


def test_03_predicate_case_insensitive():
    """Tests that the predicate returns correct values.

    tests: R-PARSER-FILTER-REGEX-001
    tests: R-PARSER-FILTER-REGEX-003
    """
    regexes = ["FIRE.*",
               "libc",
               "gcc-[6-9]",
               "gtk\\+"]
    r = RegexFilter(regexes)

    assert not r.test(dict())
    assert r.test(dict(atom="www-client/firefox-55.0"))
    assert r.test(dict(atom="glibc"))
    assert r.test(dict(atom="gcc-8.1.0"))
    assert r.test(dict(atom="GTK+"))


def test_04_predicate_case_sensitive():
    """Tests that the predicate returns correct values.

    tests: R-PARSER-FILTER-REGEX-001
    tests: R-PARSER-FILTER-REGEX-003
    """
    regexes = ["FIRE.*",
               "libc",
               "gcc-[6-9]",
               "gtk\\+"]
    r = RegexFilter(regexes, case_sensitive=True)

    assert not r.test(dict())
    assert not r.test(dict(atom="www-client/firefox-55.0"))
    assert r.test(dict(atom="glibc"))
    assert r.test(dict(atom="gcc-8.1.0"))
    assert not r.test(dict(atom="GTK+"))
