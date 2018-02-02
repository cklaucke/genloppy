from genloppy.parser.emerge_log import EmergeLogParser

from io import StringIO
from re import compile as re_compile

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
    Tests that after subscribing the parser returns items for a proper emerge log.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-006
    tests: R-PARSER-ELOG-007
    tests: R-PARSER-ELOG-009
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = []

    def collect_items(_item):
        items.append(_item)

    elp.subscribe(collect_items, "merge")
    elp.subscribe(collect_items, "unmerge")
    elp.subscribe(collect_items, "sync")
    elp.parse(good_elog)

    assert len(items) == 6

    item = items[0]
    assert item["timestamp"] == 1507734360
    assert item["repo_name"] == "gentoo"

    item = items[1]
    assert item["timestamp"] == 1507735236
    assert item["name"] == "sys-devel/gcc-config"
    assert item["version"] == "1.7.3"

    item = items[2]
    assert item["timestamp_begin"] == 1507735226
    assert item["timestamp_end"] == 1507735239
    assert item["name"] == "sys-devel/gcc-config"
    assert item["version"] == "1.8-r1"

    item = items[3]
    assert item["timestamp"] == 1507735248
    assert item["name"] == "app-laptop/laptop-mode-tools"
    assert item["version"] == "1.70"

    item = items[4]
    assert item["timestamp_begin"] == 1507735239
    assert item["timestamp_end"] == 1507735250
    assert item["name"] == "app-laptop/laptop-mode-tools"
    assert item["version"] == "1.71"

    item = items[5]
    assert item["timestamp"] == 1508345663
    assert item["repo_name"] == "gentoo"


def test_01b_elog_good_mode_merge():
    """
    Tests that after subscribing to 'merge'
    the parser returns dict for a proper emerge log.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-004
    tests: R-PARSER-ELOG-007
    tests: R-PARSER-ELOG-009
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = []
    elp.subscribe(items.append, "merge")
    elp.parse(good_elog)

    assert len(items) == 2

    item = items[0]
    assert item["timestamp_begin"] == 1507735226
    assert item["timestamp_end"] == 1507735239
    assert item["name"] == "sys-devel/gcc-config"
    assert item["version"] == "1.8-r1"

    item = items[1]
    assert item["timestamp_begin"] == 1507735239
    assert item["timestamp_end"] == 1507735250
    assert item["name"] == "app-laptop/laptop-mode-tools"
    assert item["version"] == "1.71"


def test_01c_elog_good_mode_unmerge():
    """
    Tests that after subscribing to 'unmerge'
    the parser returns dict for a proper emerge log.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-005
    tests: R-PARSER-ELOG-007
    tests: R-PARSER-ELOG-009
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = []
    elp.subscribe(items.append, "unmerge")
    elp.parse(good_elog)

    assert len(items) == 2

    item = items[0]
    assert item["timestamp"] == 1507735236
    assert item["name"] == "sys-devel/gcc-config"
    assert item["version"] == "1.7.3"

    item = items[1]
    assert item["timestamp"] == 1507735248
    assert item["name"] == "app-laptop/laptop-mode-tools"
    assert item["version"] == "1.70"


def test_01d_elog_good_mode_sync():
    """
    Tests that after subscribing to 'sync' the parser
    returns dict for a proper emerge log.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    tests: R-PARSER-ELOG-006
    tests: R-PARSER-ELOG-007
    tests: R-PARSER-ELOG-009
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()
    items = []
    elp.subscribe(items.append, "sync")
    elp.parse(good_elog)

    assert len(items) == 2

    item = items[0]
    assert item["timestamp"] == 1507734360
    assert item["repo_name"] == "gentoo"

    item = items[1]
    assert item["timestamp"] == 1508345663
    assert item["repo_name"] == "gentoo"


def test_01e_elog_good_no_subscriptions():
    """
    Tests that an exception is raised when
    trying to parse without subscribing.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()

    with nose.tools.assert_raises(RuntimeError):
        elp.parse(good_elog)


def test_02_elp_malformed_patterns():
    """
    Tests that the parser raises an exception,
    if more than one regular expression matches for a single line.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-003
    """
    good_elog = StringIO(ELOG_GOOD)

    class MalformedEmergeLogParser(EmergeLogParser):
        MERGE_BEGIN_PATTERN = re_compile("^([0-9]+).*$")
        MERGE_END_PATTERN = re_compile("^([0-9][0-9]*).*$")

    melp = MalformedEmergeLogParser()
    items = []
    melp.subscribe(items.append, "merge")

    with nose.tools.assert_raises(RuntimeError):
        melp.parse(good_elog)


def test_03_elog_incomplete_entries():
    """
    Tests that log entries are ignored if emerge log has
    - a merge begin without a merge end, or
    - a merge end without a merge begin.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-004
    """
    elp = EmergeLogParser()

    incomplete_elog = StringIO(ELOG_END_WO_BEGIN)
    items = []
    elp.subscribe(items.append, "merge")
    elp.parse(incomplete_elog)
    assert not items

    incomplete_elog = StringIO(ELOG_BEGIN_WO_END)
    items = []
    elp.parse(incomplete_elog)
    assert not items


def test_04_elog_mismatched_entries():
    """
    Tests that log entries are ignored if atom base, atom version and count
    from merge begin and merge end do not match.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-004
    """
    elp = EmergeLogParser()

    incomplete_elog = StringIO(ELOG_BEGIN_END_MISMATCH1)
    items = []
    elp.subscribe(items.append, "merge")
    elp.parse(incomplete_elog)
    assert not items

    incomplete_elog = StringIO(ELOG_BEGIN_END_MISMATCH2)
    items = []
    elp.parse(incomplete_elog)
    assert not items


def test_05_subscribe_unknown_mode():
    """
    Tests that an exception is raised if trying to subscribe to an unknown mode.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-007
    """
    elp = EmergeLogParser()

    with nose.tools.assert_raises(RuntimeError):
        elp.subscribe(lambda x: x, "void")


def test_06a_unsubscribe_invalid_modes():
    """
    Tests that an exception is raised if trying
    to unsubscribe from a mode which was not subscribed to or is unknown.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-008
    """
    elp = EmergeLogParser()

    with nose.tools.assert_raises(RuntimeError):
        elp.unsubscribe(lambda x: x, "merge")

    with nose.tools.assert_raises(RuntimeError):
        elp.unsubscribe(lambda x: x, "void")


def test_06b_unsubscribe_unknown_callback_specific_mode():
    """
    Tests that an exception is raised if trying
    to unsubscribe an unknown callback from a specific mode.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-008
    """
    elp = EmergeLogParser()

    elp.subscribe(lambda x: x, "merge")

    with nose.tools.assert_raises(RuntimeError):
        elp.unsubscribe(lambda x: x, "merge")


def test_06c_unsubscribe_unknown_callback():
    """
    Tests that an exception is raised if trying to unsubscribe an unknown callback.

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-008
    """
    elp = EmergeLogParser()

    elp.subscribe(lambda x: x, "merge")

    with nose.tools.assert_raises(RuntimeError):
        elp.unsubscribe(lambda x: x)


def test_07a_subscribe_unsubscribe():
    """
    Tests that subscribing and unsubscribing work as expected:
    - subscribe to two modes
    - parse returns items for both modes
    - unsubscribe one mode
    - parse returns items for one mode only

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-007
    tests: R-PARSER-ELOG-008
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()

    class ItemCollector:
        def __init__(self):
            self.items = []

        def __call__(self, _item):
            self.items.append(_item)

    mic = ItemCollector()
    uic = ItemCollector()

    elp.subscribe(mic, "merge")
    elp.subscribe(uic, "unmerge")
    elp.parse(good_elog)

    assert len(mic.items) == 2
    for _item in mic.items:
        nose.tools.assert_true("timestamp_begin" in _item.keys())
        nose.tools.assert_true("timestamp_end" in _item.keys())
    assert len(uic.items) == 2
    for _item in uic.items:
        nose.tools.assert_true("timestamp" in _item.keys())

    mic.items.clear()
    uic.items.clear()

    elp.unsubscribe(uic)

    good_elog = StringIO(ELOG_GOOD)
    elp.parse(good_elog)

    assert len(mic.items) == 2
    for _item in mic.items:
        nose.tools.assert_true("timestamp_begin" in _item.keys())
        nose.tools.assert_true("timestamp_end" in _item.keys())
    assert not uic.items


def test_07b_multiple_subscribes():
    """
    Tests that subscribing and unsubscribing work as expected:
    - subscribe to the same mode w/ two different callbacks
    - parse returns items for both callbacks
    - unsubscribing succeeds

    tests: R-PARSER-ELOG-001
    tests: R-PARSER-ELOG-007
    tests: R-PARSER-ELOG-008
    """
    good_elog = StringIO(ELOG_GOOD)

    elp = EmergeLogParser()

    class ItemCollector:
        def __init__(self):
            self.items = []

        def __call__(self, _item):
            self.items.append(_item)

    mic1 = ItemCollector()
    mic2 = ItemCollector()

    elp.subscribe(mic1, "merge")
    elp.subscribe(mic2, "merge")
    elp.parse(good_elog)
    elp.unsubscribe(mic1, "merge")
    elp.unsubscribe(mic2, "merge")

    assert len(mic1.items) == 2
    for _item in mic1.items:
        nose.tools.assert_true("timestamp_begin" in _item.keys())
        nose.tools.assert_true("timestamp_end" in _item.keys())
    assert mic1.items == mic2.items
