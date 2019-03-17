from io import StringIO

import pytest

from genloppy.parser.emerge_log import EmergeLogParser, EmergeLogParserError

ELOG_GOOD = """1507734360: === Sync completed for gentoo
1507734361:  *** terminating.
1507735118: Started emerge on: Oct 11, 2017 17:18:38
1507735118:  *** emerge --update --verbose --deep @world
1507735226:  >>> emerge (1 of 2) sys-devel/gcc-config-1.8-r1 to /
1507735227:  === (1 of 2) Cleaning (sys-devel/gcc-config-1.8-r1::/usr/portage/sys-devel/gcc-config/gcc-config-1.8-r1.ebuild)
1507735227:  === (1 of 2) Compiling/Merging (sys-devel/gcc-config-1.8-r1::/usr/portage/sys-devel/gcc-config/gcc-config-1.8-r1.ebuild)
1507735231:  === (1 of 2) Merging (sys-devel/gcc-config-1.8-r1::/usr/portage/sys-devel/gcc-config/gcc-config-1.8-r1.ebuild)
1507735234:  >>> AUTOCLEAN: sys-devel/gcc-config:0
1507735234:  === Unmerging... (sys-devel/gcc-config-1.7.3)
1507735236:  >>> unmerge success: sys-devel/gcc-config-1.7.3
1507735239:  === (1 of 2) Post-Build Cleaning (sys-devel/gcc-config-1.8-r1::/usr/portage/sys-devel/gcc-config/gcc-config-1.8-r1.ebuild)
1507735239:  ::: completed emerge (1 of 2) sys-devel/gcc-config-1.8-r1 to /
1507735239:  >>> emerge (2 of 2) app-laptop/laptop-mode-tools-1.71 to /
1507735239:  === (2 of 2) Cleaning (app-laptop/laptop-mode-tools-1.71::/usr/portage/app-laptop/laptop-mode-tools/laptop-mode-tools-1.71.ebuild)
1507735239:  === (2 of 2) Compiling/Merging (app-laptop/laptop-mode-tools-1.71::/usr/portage/app-laptop/laptop-mode-tools/laptop-mode-tools-1.71.ebuild)
1507735244:  === (2 of 2) Merging (app-laptop/laptop-mode-tools-1.71::/usr/portage/app-laptop/laptop-mode-tools/laptop-mode-tools-1.71.ebuild)
1507735246:  >>> AUTOCLEAN: app-laptop/laptop-mode-tools:0
1507735246:  === Unmerging... (app-laptop/laptop-mode-tools-1.70)
1507735248:  >>> unmerge success: app-laptop/laptop-mode-tools-1.70
1507735250:  === (2 of 2) Post-Build Cleaning (app-laptop/laptop-mode-tools-1.71::/usr/portage/app-laptop/laptop-mode-tools/laptop-mode-tools-1.71.ebuild)
1507735250:  ::: completed emerge (2 of 2) app-laptop/laptop-mode-tools-1.71 to /
1507735250:  *** Finished. Cleaning up...
1507735252:  *** exiting successfully.
1507735252:  *** terminating.
1508345663: === Sync completed for gentoo"""

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


def test_01a_good_elog_parses_successful():
    """
    Tests that the parser matches the entry types and delegates to the given handler for a proper emerge log.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-002
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    tests: R-PARSER-ELOG-007
    """

    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    entry_handler = MockedEntryHandler()
    elp.handler = entry_handler

    elp.parse(good_elog)

    entries = entry_handler.entries
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
    Tests that the parser raises if an entry handler was not given.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    """
    elp = EmergeLogParser()

    with pytest.raises(EmergeLogParserError):
        elp.parse(StringIO(ELOG_GOOD))


def test_01c_known_entry_types():
    """
    Tests that all known entry types are returned.

    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    tests: R-PARSER-ELOG-007
    tests: R-PARSER-ELOG-009
    """
    elp = EmergeLogParser()

    known_entry_types = set(elp.entry_types)
    assert known_entry_types == {"merge_begin", "merge_end", "sync", "unmerge"}


def test_02_optional_configuration():
    """
    Tests that parser allows for optional configuration of filters.

    tests: R-PARSER-ELOG-008
    """
    elp = EmergeLogParser()
    elp.configure(foo="bar")
