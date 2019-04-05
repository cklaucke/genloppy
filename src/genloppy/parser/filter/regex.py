import re

from genloppy.parser.entry_handler_wrapper import EntryHandlerWrapper


class RegexFilter(EntryHandlerWrapper):
    """
    Filters entry events for given regular expressions.

    realizes: R-PARSER-FILTER-REGEX-001
    """

    def __init__(self, regular_expressions, **kwargs):
        """Initializes the filter with the given regular expressions.

        realizes: R-PARSER-FILTER-REGEX-002
        """
        super().__init__()
        self.case_sensitive = kwargs.get("case_sensitive", False)
        self.regexes = self._store_regexes(set(regular_expressions), self.case_sensitive)

    @staticmethod
    def _store_regexes(regular_expressions, case_sensitive=False):
        regexes = []
        malformed_regexes = []

        for regular_expression in regular_expressions:
            try:
                regexes.append(re.compile(regular_expression, 0 if case_sensitive else re.IGNORECASE))
            except re.error:
                malformed_regexes.append(regular_expression)

        if malformed_regexes:
            raise RuntimeError("Malformed regular expressions given: '{}'. Aborting!"
                               .format(", ".join(malformed_regexes)))

        return regexes

    def test(self, properties):
        """Tests for regular expression matches

        :param properties: tokens (key-value) of the entry event
        :return: True if any regular expression matches, False otherwise

        realizes: R-PARSER-FILTER-REGEX-003
        """
        atom = properties.get("atom")
        if atom:
            return any(map(lambda regex: regex.search(atom), self.regexes))
        else:
            return False
