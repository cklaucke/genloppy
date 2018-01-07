#!/usr/bin/env python3

__author__ = "cklaucke"


from genloppy.parser.emerge_log import EmergeLogParser
from genloppy.item import MergeItem, SyncItem, UnmergeItem

from io import StringIO
from re import compile

import nose.tools

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


def test_01a_elog_good_mode_any():
    """
    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = list(elp.parse(good_elog))
    assert len(items) == 6

    item = items[0]
    assert isinstance(item, SyncItem)
    assert item.timestamp == 1507734360
    assert item.repo_name == "gentoo"

    item = items[1]
    assert isinstance(item, UnmergeItem)
    assert item.timestamp == 1507735236
    assert item.name == "sys-devel/gcc-config"
    assert item.version == "1.7.3"

    item = items[2]
    assert isinstance(item, MergeItem)
    assert item.timestamp == 1507735226
    assert item.timestamp_end == 1507735239
    assert item.duration == 13
    assert item.name == "sys-devel/gcc-config"
    assert item.version == "1.8-r1"

    item = items[3]
    assert isinstance(item, UnmergeItem)
    assert item.timestamp == 1507735248
    assert item.name == "app-laptop/laptop-mode-tools"
    assert item.version == "1.70"

    item = items[4]
    assert isinstance(item, MergeItem)
    assert item.timestamp == 1507735239
    assert item.timestamp_end == 1507735250
    assert item.duration == 11
    assert item.name == "app-laptop/laptop-mode-tools"
    assert item.version == "1.71"

    item = items[5]
    assert isinstance(item, SyncItem)
    assert item.timestamp == 1508345663
    assert item.repo_name == "gentoo"


def test_01b_elog_good_mode_merge():
    """
    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = list(elp.parse(good_elog, mode='merge'))
    assert len(items) == 2

    item = items[0]
    assert isinstance(item, MergeItem)
    assert item.timestamp == 1507735226
    assert item.timestamp_end == 1507735239
    assert item.duration == 13
    assert item.name == "sys-devel/gcc-config"
    assert item.version == "1.8-r1"

    item = items[1]
    assert isinstance(item, MergeItem)
    assert item.timestamp == 1507735239
    assert item.timestamp_end == 1507735250
    assert item.duration == 11
    assert item.name == "app-laptop/laptop-mode-tools"
    assert item.version == "1.71"


def test_01c_elog_good_mode_unmerge():
    """
    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = list(elp.parse(good_elog, mode='unmerge'))
    assert len(items) == 2

    item = items[0]
    assert isinstance(item, UnmergeItem)
    assert item.timestamp == 1507735236
    assert item.name == "sys-devel/gcc-config"
    assert item.version == "1.7.3"

    item = items[1]
    assert isinstance(item, UnmergeItem)
    assert item.timestamp == 1507735248
    assert item.name == "app-laptop/laptop-mode-tools"
    assert item.version == "1.70"


def test_01d_elog_good_mode_sync():
    """
    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = list(elp.parse(good_elog, mode='sync'))
    assert len(items) == 2

    item = items[0]
    assert isinstance(item, SyncItem)
    assert item.timestamp == 1507734360
    assert item.repo_name == "gentoo"

    item = items[1]
    assert isinstance(item, SyncItem)
    assert item.timestamp == 1508345663
    assert item.repo_name == "gentoo"


def test_02_elp_malformed_patterns():
    """
    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    """
    good_elog = StringIO(ELOG_GOOD)

    class MalformedEmergeLogParser(EmergeLogParser):
        MERGE_BEGIN_PATTERN = compile("^([0-9]+).*$")
        MERGE_END_PATTERN = compile("^([0-9][0-9]*).*$")

    melp = MalformedEmergeLogParser()

    with nose.tools.assert_raises(RuntimeError):
        list(melp.parse(good_elog))


def test_03_elog_incomplete_entries():
    """
    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-004
    """
    elp = EmergeLogParser()

    incomplete_elog = StringIO(ELOG_END_WO_BEGIN)
    assert len(list(elp.parse(incomplete_elog))) == 0

    incomplete_elog = StringIO(ELOG_BEGIN_WO_END)
    assert len(list(elp.parse(incomplete_elog))) == 0


def test_04_elog_mismatched_entries():
    """
    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-004
    """
    elp = EmergeLogParser()

    incomplete_elog = StringIO(ELOG_BEGIN_END_MISMATCH1)
    assert len(list(elp.parse(incomplete_elog))) == 0

    incomplete_elog = StringIO(ELOG_BEGIN_END_MISMATCH2)
    assert len(list(elp.parse(incomplete_elog))) == 0
