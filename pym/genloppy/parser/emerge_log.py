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

    class Subscription:
        """
        Holds and manages callbacks for a given pattern callback map.
        """
        def __init__(self, pattern_callbacks):
            self._pattern_callbacks = pattern_callbacks
            self._callbacks = []

        @property
        def pattern_callbacks(self):
            """Returns the pattern callbacks dict."""
            return self._pattern_callbacks

        @property
        def callbacks(self):
            """Returns the subscription callbacks."""
            return self._callbacks

        def add_callback(self, callback):
            """Adds a callback to the subscription."""
            self._callbacks.append(callback)

        def remove_callback(self, callback):
            """Removes a callback from the subscription."""
            self._callbacks.remove(callback)

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

        self.subscriptions = {}

        self.current_merge_begin_match = None

    def subscribe(self, callback, mode):
        """Subscribes the callback for a given mode.

        realizes: R-PARSER-ELOG-007"""
        if mode not in self._modes.keys():
            raise RuntimeError("Cannot subscribe to unknown mode '{}'.".format(mode))

        subscription = self.subscriptions.get(mode)

        if not subscription:
            subscription = EmergeLogParser.Subscription(self._modes[mode])
            self.subscriptions[mode] = subscription

        subscription.add_callback(callback)

    def unsubscribe(self, callback, mode=None):
        """Unsubscribes the callback from a given mode.

        realizes: R-PARSER-ELOG-008"""
        def _unsubscribe(_callback, _mode):
            if _callback not in self.subscriptions[_mode].callbacks:
                raise RuntimeError("Cannot unsubscribe! '{}' not found in subscriptions for mode {}."
                                   .format(_callback, _mode))

            self.subscriptions[_mode].remove_callback(_callback)

        modes_found = []
        if mode:
            if mode not in self._modes.keys() or mode not in self.subscriptions:
                raise RuntimeError("Cannot unsubscribe to unknown or unsubscribed mode '{}'.".format(mode))

            _unsubscribe(callback, mode)
            modes_found.append(mode)
        else:
            for subscription_mode, subscription in self.subscriptions.items():
                if callback in subscription.callbacks:
                    modes_found.append(subscription_mode)
                    _unsubscribe(callback, subscription_mode)

            if not modes_found:
                raise RuntimeError("Cannot unsubscribe! '{}' not found in any subscription."
                                   .format(callback))

        # clean-up subscriptions
        for subscription_mode in modes_found:
            if not self.subscriptions[subscription_mode].callbacks:
                self.subscriptions.pop(subscription_mode)

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

    def parse(self, stream):
        """Parse a given stream for items using the defined patterns and callbacks.

        realizes: R-PARSER-ELOG-003
        realizes: R-PARSER-ELOG-009"""
        self.current_merge_begin_match = None

        if not self.subscriptions:
            raise RuntimeError("No subscription provided.")

        def process_entry(_line):
            matched = False
            # always iterate through all patterns to detect corrupt log files
            for subscription in self.subscriptions.values():
                for pattern, pattern_callback in subscription.pattern_callbacks.items():
                    match = pattern.match(_line)

                    if match:
                        if matched:
                            raise RuntimeError("Pattern malformed. More than one pattern matched at a time.")

                        matched = True
                        result = pattern_callback(match)

                        if result:
                            for subscription_callback in subscription.callbacks:
                                subscription_callback(result)

        for line in stream:
            process_entry(line)
