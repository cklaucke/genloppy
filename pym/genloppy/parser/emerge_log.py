import re

from genloppy.parser.pms import \
    MERGE_BEGIN_PATTERN, MERGE_END_PATTERN, \
    UNMERGE_PATTERN, SYNC_COMPLETED_PATTERN


class EmergeLogParserError(BaseException):
    pass


class EmergeLogParser:
    """
    Extracts relevant items from the emerge log

    realizes: R-PARSER-ELOG-001
    realizes: R-PARSER-ELOG-004
    realizes: R-PARSER-ELOG-005
    realizes: R-PARSER-ELOG-006
    realizes: R-PARSER-ELOG-007
    """
    ENTRY_TYPE_PATTERN = {
        "merge_begin": re.compile(MERGE_BEGIN_PATTERN),
        "merge_end": re.compile(MERGE_END_PATTERN),
        "unmerge": re.compile(UNMERGE_PATTERN),
        "sync": re.compile(SYNC_COMPLETED_PATTERN),
    }

    def __init__(self, handler=None):
        self._handler = handler

    def configure(self, **kwargs):
        """Configures optional parser filters

        realizes: R-PARSER-LOG-008
        """
        pass

    @property
    def entry_types(self):
        """Gets known entry types.

        :return: an iterable of known entry types
        realizes: R-PARSER-ELOG-009
        """
        return self.ENTRY_TYPE_PATTERN.keys()

    @property
    def handler(self):
        """Gets the entry handler.

        :return: the entry handler.

        realizes: R-PARSER-ELOG-002
        """
        return self._handler

    @handler.setter
    def handler(self, handler):
        """Sets the entry handler.

        :param handler: An entry handler

        realizes: R-PARSER-ELOG-002
        """
        self._handler = handler

    def parse(self, stream):
        """Parse a given stream for items using the defined patterns and callbacks.

        :param stream: a file-like object o parse

        realizes: R-PARSER-ELOG-003
        """

        if self.handler is None:
            raise EmergeLogParserError("Entry handler not given!")

        # TODO: ask handler about listened event types to skip unneeded regex matches

        for line in stream:
            for entry_type, pattern in self.ENTRY_TYPE_PATTERN.items():
                match = pattern.match(line)

                if match:
                    self.handler.entry(entry_type, match.groupdict())
