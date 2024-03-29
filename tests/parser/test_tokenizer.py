import re
from io import StringIO

import pytest

from genloppy.parser.tokenizer import Tokenizer, TokenizerError


class MockEntryHandler:
    def __init__(self, keys):
        self._listener = dict.fromkeys(keys, "")
        self.entries = []

    @property
    def listener(self):
        return self._listener

    def entry(self, entry_type, properties):
        self.entries.append((entry_type, properties))


def test_01_missing_entry_handler_raises():
    """Test that a missing entry handler raises.

    tests: R-PARSER-TOKENIZER-001
    tests: R-PARSER-TOKENIZER-002
    tests: R-PARSER-TOKENIZER-003
    tests: R-PARSER-TOKENIZER-004
    """
    t = Tokenizer({})

    with pytest.raises(TokenizerError) as cm:
        t.tokenize(StringIO())

    assert cm.value.args[0] == "Entry entry_handler not given!"


def test_02_unknown_entry_raises():
    """Tests that an unknown entry raises.

    tests: R-PARSER-TOKENIZER-001
    tests: R-PARSER-TOKENIZER-002
    tests: R-PARSER-TOKENIZER-003
    tests: R-PARSER-TOKENIZER-004
    """
    meh = MockEntryHandler(["a"])
    t = Tokenizer({}, meh)

    with pytest.raises(TokenizerError) as cm:
        t.tokenize(StringIO())

    assert cm.value.args[0] == "Unknown registered entry type"


def test_03_simple_tokenization_succeeds(capsys):
    """Tests that a simple tokenization succeeds.

    tests: R-PARSER-TOKENIZER-001
    tests: R-PARSER-TOKENIZER-002
    tests: R-PARSER-TOKENIZER-003
    tests: R-PARSER-TOKENIZER-004
    """
    meh = MockEntryHandler(["a"])
    t = Tokenizer({"a": re.compile("^a$")}, meh)

    t.tokenize(StringIO("a"))

    captured = capsys.readouterr()
    assert len(meh.entries) == 1
    assert meh.entries[0] == ("a", {})
    assert captured.out == ""


def test_04_complex_tokenization_succeeds(capsys):
    """Tests that a complex tokenization succeeds.

    tests: R-PARSER-TOKENIZER-001
    tests: R-PARSER-TOKENIZER-002
    tests: R-PARSER-TOKENIZER-003
    tests: R-PARSER-TOKENIZER-004
    """
    meh = MockEntryHandler(["a"])
    t = Tokenizer({"a": re.compile("^(?P<number>[0-9]+)a$"), "b": re.compile("^(?P<number>[0-9]+)b$")}, meh, echo=True)

    t.tokenize(StringIO("1337a\n42b"))

    captured = capsys.readouterr()
    assert len(meh.entries) == 1
    assert meh.entries[0] == ("a", {"number": "1337"})
    assert captured.out == "1337a\n"


def test_05_optional_configuration():
    """Tests that tokenizer allows for optional configuration of filters.

    tests: R-PARSER-TOKENIZER-001
    tests: R-PARSER-TOKENIZER-005
    """
    t = Tokenizer({}, None)
    t.configure(foo="bar")


def test_06_entry_handler_property():
    """Tests that getter and setter for entry_handler works.

    tests: R-PARSER-TOKENIZER-001
    tests: R-PARSER-TOKENIZER-002
    """
    meh = MockEntryHandler([])
    t = Tokenizer({}, meh)
    assert t.entry_handler == meh

    meh2 = MockEntryHandler(["a"])
    t.entry_handler = meh2
    assert t.entry_handler == meh2
