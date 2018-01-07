"""
Provides parser for emerge logs

realizes: R-PARSER-ELOG-001
"""

__author__ = "cklaucke"

from genloppy.item import MergeItem, SyncItem, UnmergeItem

import re


class EmergeLogParser:
    """
    Extracts relevant items from the emerge log

    realizes: R-PARSER-ELOG-001
    realizes: R-PARSER-ELOG-002
    realizes: R-PARSER-ELOG-004
    """

    # for specification see https://dev.gentoo.org/~ulm/pms/head/pms.html
    CATEGORY_PATTERN = r"[A-Za-z0-9_][A-Za-z0-9+_.-]*"
    PACKAGE_NAME_PATTERN = r"[A-Za-z0-9_][A-Za-z0-9+_-]*"
    # according to spec "-[0-9]" starts a version (see. PMS section 3.2)
    ATOM_PATTERN = r"(?P<atom_base>" + CATEGORY_PATTERN + r"/" \
                   + PACKAGE_NAME_PATTERN + r")(?=-[0-9])-(?P<atom_version>[^\s]+)"

    TIMESTAMP_PATTERN = r"(?P<timestamp>[0-9]+)"
    COUNT_PATTERN = r"\((?P<count_n>[0-9]+) of (?P<count_m>[0-9]+)\)"

    # patterns for log entry lines
    MERGE_BEGIN_PATTERN = re.compile(r"^" + TIMESTAMP_PATTERN + r": {2}>>> emerge "
                                     + COUNT_PATTERN + r" " + ATOM_PATTERN + r" to .*$")

    MERGE_END_PATTERN = re.compile(r"^" + TIMESTAMP_PATTERN + r": {2}::: completed emerge "
                                   + COUNT_PATTERN + r" " + ATOM_PATTERN + r" to .*$")

    SYNC_COMPLETED_PATTERN = re.compile(r"^" + TIMESTAMP_PATTERN +
                                        r": === Sync completed for (?P<repo_name>.*)$")

    UNMERGE_PATTERN = re.compile(r"^" + TIMESTAMP_PATTERN + r": {2}>>> unmerge success: " +
                                 ATOM_PATTERN + r"$")

    def __init__(self):
        self._modes = {
            "merge": {
                self.MERGE_BEGIN_PATTERN: self.merge_begin_log_entry,
                self.MERGE_END_PATTERN: self.merge_end_log_entry,
            },
            "unmerge": {
                self.UNMERGE_PATTERN: self.unmerge_log_entry,
            },
            "sync": {
                self.SYNC_COMPLETED_PATTERN: self.sync_log_entry,
            }
        }

        self.current_merge_begin_match = None

    def get_pattern_callbacks(self, mode):
        """Return pattern callbacks for a given mode."""
        if mode == "any":
            pattern_callbacks = {}
            for d in self._modes.values():
                pattern_callbacks.update(d)
        else:
            pattern_callbacks = self._modes[mode]
        return pattern_callbacks

    def merge_begin_log_entry(self, match):
        """Save the current match to be processed by a corresponding
        merge end entry.

        realizes: R-PARSER-ELOG-004"""
        self.current_merge_begin_match = match

    def merge_end_log_entry(self, match):
        """Process merge end entry match and return an item if a corresponding
        merge begin entry was found beforehand.

        realizes: R-PARSER-ELOG-004"""
        item = None

        if self.current_merge_begin_match:
            # consistency check: count, atom and version shall match
            if self.current_merge_begin_match.groups()[1:] == match.groups()[1:]:
                item = MergeItem(int(self.current_merge_begin_match.group('timestamp')),
                                 int(match.group('timestamp')),
                                 self.current_merge_begin_match.group('atom_base'),
                                 self.current_merge_begin_match.group('atom_version'))

        self.current_merge_begin_match = None
        return item

    @staticmethod
    def sync_log_entry(match):
        """Process sync entry match and return an item.

        realizes: R-PARSER-ELOG-006"""
        return SyncItem(int(match.group('timestamp')), match.group('repo_name'))

    @staticmethod
    def unmerge_log_entry(match):
        """Process unmerge entry match.

        realizes: R-PARSER-ELOG-005"""
        return UnmergeItem(int(match.group('timestamp')),
                           match.group('atom_base'),
                           match.group('atom_version'))

    def parse(self, stream, mode='any'):
        """Parse a given stream for items using the defined patterns and callbacks.

        realizes: R-PARSER-ELOG-003"""
        pattern_callbacks = self.get_pattern_callbacks(mode)

        self.current_merge_begin_match = None

        for line in stream:
            matched = False

            # always iterate through all patterns to detect corrupt log files
            for pattern, callback in pattern_callbacks.items():
                match = pattern.match(line)

                if match:
                    if matched:
                        raise RuntimeError("Pattern malformed. More than one pattern matched at a time.")

                    matched = True
                    result = callback(match)
                    if result:
                        yield result
