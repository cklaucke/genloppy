class TokenizerError(BaseException):
    pass


class Tokenizer:
    """
    Configurable tokenizer

    realizes: R-PARSER-TOKENIZER-001
    realizes: R-PARSER-TOKENIZER-002
    realizes: R-PARSER-TOKENIZER-003
    """

    def __init__(self, entry_type_pattern, entry_handler, echo=False):
        self._entry_type_pattern = dict(entry_type_pattern)
        self._entry_handler = entry_handler
        self.echo = echo

    def configure(self, **kwargs):
        """Configures optional parser filters

        realizes: R-PARSER-TOKENIZER-005
        """
        pass

    @property
    def entry_handler(self):
        """Gets the entry handler.

        :return: the entry_handler.

        realizes: R-PARSER-TOKENIZER-002
        """
        return self._entry_handler

    def tokenize(self, stream):
        """Tokenize a given stream using the configured patterns.

        :param stream: a file-like object o tokenize

        realizes: R-PARSER-TOKENIZER-004
        """

        if self.entry_handler is None:
            raise TokenizerError("Entry entry_handler not given!")

        listened_entry_types = set(self.entry_handler.listener.keys())
        unknown_entry_types = listened_entry_types.difference(self._entry_type_pattern.keys())
        if unknown_entry_types:
            raise TokenizerError("Unknown registered entry type")

        entry_type_pattern = dict(
            item for item in self._entry_type_pattern.items()
            if item[0] in listened_entry_types)

        for line in stream:
            for entry_type, pattern in entry_type_pattern.items():
                match = pattern.match(line)

                if match:
                    self.entry_handler.entry(entry_type, match.groupdict())
                    if self.echo:
                        print(line)
