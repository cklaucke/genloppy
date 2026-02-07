from io import StringIO
from pathlib import Path

import pytest

from genloppy.parser.entry_handler import EntryHandler
from genloppy.parser.pms import EMERGE_LOG_ENTRY_TYPES
from genloppy.parser.tokenizer import Tokenizer, TokenizerError

ELOG_END_WO_BEGIN = """1507735239:  ::: completed emerge (1 of 2) sys-devel/gcc-config-1.8-r1 to /"""

ELOG_BEGIN_WO_END = """1507735226:  >>> emerge (1 of 2) sys-devel/gcc-config-1.8-r1 to /
1507735226:  >>> emerge (1 of 2) sys-devel/gcc-config-1.8-r1 to /"""

ELOG_BEGIN_END_MISMATCH1 = """1507735226:  >>> emerge (1 of 2) sys-devel/gcc-config-1.9.1 to /
1507735239:  ::: completed emerge (1 of 2) sys-devel/gcc-config-1.8-r1 to /"""

ELOG_BEGIN_END_MISMATCH2 = """1507735226:  >>> emerge (13 of 37) sys-devel/gcc-config-1.8-r1 to /
1507735239:  ::: completed emerge (1 of 2) sys-devel/gcc-config-1.8-r1 to /"""


class MockedEntryHandler:
    def __init__(self):
        self.entries = []

    def entry(self, entry_type, properties):
        self.entries.append((entry_type, properties))

    @property
    def listener(self):
        return {"merge_begin": None, "merge_end": None, "sync": None, "unmerge": None}


def test_01a_good_elog_parses_successful():  # noqa: PLR0915
    """
    Tests that the parser matches the entry types and delegates to the given entry_handler for a proper emerge log.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-002
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    tests: R-PARSER-ELOG-007
    """

    elp = Tokenizer(EMERGE_LOG_ENTRY_TYPES, MockedEntryHandler())

    with (Path(__file__).parent / "good_emerge.log").open() as fh:
        elp.tokenize(fh)

    entries = elp.entry_handler.entries
    assert len(entries) == 8

    entry = entries[0]
    assert entry[0] == "sync"
    assert entry[1]["timestamp"] == "1507734360"
    assert entry[1]["repo_name"] == "gentoo"

    entry = entries[1]
    assert entry[0] == "merge_begin"
    assert entry[1]["timestamp"] == "1507735226"
    assert entry[1]["atom_base"] == "sys-devel/gcc-config"
    assert entry[1]["atom_version"] == "1.8-r1"
    assert entry[1]["count_n"] == "1"
    assert entry[1]["count_m"] == "2"

    entry = entries[2]
    assert entry[0] == "unmerge"
    assert entry[1]["timestamp"] == "1507735236"
    assert entry[1]["atom_base"] == "sys-devel/gcc-config"
    assert entry[1]["atom_version"] == "1.7.3"

    entry = entries[3]
    assert entry[0] == "merge_end"
    assert entry[1]["timestamp"] == "1507735239"
    assert entry[1]["atom_base"] == "sys-devel/gcc-config"
    assert entry[1]["atom_version"] == "1.8-r1"
    assert entry[1]["count_n"] == "1"
    assert entry[1]["count_m"] == "2"

    entry = entries[4]
    assert entry[0] == "merge_begin"
    assert entry[1]["timestamp"] == "1507735239"
    assert entry[1]["atom_base"] == "app-laptop/laptop-mode-tools"
    assert entry[1]["atom_version"] == "1.71"
    assert entry[1]["count_n"] == "2"
    assert entry[1]["count_m"] == "2"

    entry = entries[5]
    assert entry[0] == "unmerge"
    assert entry[1]["timestamp"] == "1507735248"
    assert entry[1]["atom_base"] == "app-laptop/laptop-mode-tools"
    assert entry[1]["atom_version"] == "1.70"

    entry = entries[6]
    assert entry[0] == "merge_end"
    assert entry[1]["timestamp"] == "1507735250"
    assert entry[1]["atom_base"] == "app-laptop/laptop-mode-tools"
    assert entry[1]["atom_version"] == "1.71"
    assert entry[1]["count_n"] == "2"
    assert entry[1]["count_m"] == "2"

    entry = entries[7]
    assert entry[0] == "sync"
    assert entry[1]["timestamp"] == "1508345663"
    assert entry[1]["repo_name"] == "gentoo"


def test_01b_missing_handler_raises():
    """
    Tests that the parser raises if an entry entry_handler was not given.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    """
    elp = Tokenizer({}, None)

    with (Path(__file__).parent / "good_emerge.log").open() as fh, pytest.raises(TokenizerError):
        elp.tokenize(fh)


def test_02_optional_configuration():
    """
    Tests that parser allows for optional configuration of filters.

    tests: R-PARSER-ELOG-008
    """
    elp = Tokenizer({}, None)
    elp.configure(foo="bar")


def test_03_registering_unknown_entry_type_raises():
    """
    Tests that an exception is raised if trying to register for an unknown entry type.

    tests: R-PARSER-ENTRY-HANDLER-001
    tests: R-PARSER-ENTRY-HANDLER-002
    tests: R-PARSER-ENTRY-HANDLER-003
    """
    eh = EntryHandler()
    eh.register_listener(lambda x: x, "void")
    elp = Tokenizer({}, eh)

    with pytest.raises(TokenizerError):
        elp.tokenize(StringIO(""))
