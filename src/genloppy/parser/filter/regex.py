import re
from collections.abc import Iterable

from genloppy.parser.entry_handler_wrapper import EntryHandlerWrapper


class RegexFilter(EntryHandlerWrapper):
    """
    Filters entry events for given regular expressions.

    realizes: R-PARSER-FILTER-REGEX-001
    """

    def __init__(self, regular_expressions: Iterable[str], **kwargs):
        """Initializes the filter with the given regular expressions.

        realizes: R-PARSER-FILTER-REGEX-002
        """
        super().__init__(regular_expressions, **kwargs)
        self.case_sensitive: bool = kwargs.get("case_sensitive", False)
        self.regexes = self._store_regexes(set(regular_expressions), self.case_sensitive)

    @staticmethod
    def _store_regexes(regular_expressions: Iterable[str], case_sensitive: bool = False) -> list[re.Pattern[str]]:
        regexes = []
        malformed_regexes: list[str] = []

        for regular_expression in regular_expressions:
            try:
                regexes.append(re.compile(regular_expression, 0 if case_sensitive else re.IGNORECASE))
            except re.error:
                malformed_regexes.append(regular_expression)

        if malformed_regexes:
            raise RuntimeError(
                "Malformed regular expressions given: '{}'. Aborting!".format(", ".join(malformed_regexes))
            )

        return regexes

    def test(self, properties: dict[str, str]):
        """Tests for regular expression matches

        :param properties: tokens (key-value) of the entry event
        :return: True if any regular expression matches, False otherwise

        realizes: R-PARSER-FILTER-REGEX-003
        """
        atom = properties.get("atom")
        if atom:
            return any(regex.search(atom) for regex in self.regexes)
        else:
            return False
