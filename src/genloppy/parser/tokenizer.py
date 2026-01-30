import sys
from typing import TextIO


class TokenizerError(BaseException):
    pass


class Tokenizer:
    """
    Configurable tokenizer

    realizes: R-PARSER-TOKENIZER-001
    realizes: R-PARSER-TOKENIZER-002
    realizes: R-PARSER-TOKENIZER-003
    """

    def __init__(self, entry_type_pattern, entry_handler=None, *, echo=False):
        self._entry_type_pattern = dict(entry_type_pattern)
        self._entry_handler = entry_handler
        self.echo = echo

    def configure(self, **kwargs):
        """Configures optional parser filters

        realizes: R-PARSER-TOKENIZER-005
        """

    @property
    def entry_handler(self):
        """Gets the entry handler.

        :return: the entry_handler.

        realizes: R-PARSER-TOKENIZER-002
        """
        return self._entry_handler

    @entry_handler.setter
    def entry_handler(self, entry_handler):
        """Sets the entry handler.

        :param entry_handler: an entry handler to use

        realizes: R-PARSER-TOKENIZER-002
        """
        self._entry_handler = entry_handler

    def tokenize(self, stream: TextIO):
        """Tokenize a given stream using the configured patterns.

        :param stream: a file-like object o tokenize

        realizes: R-PARSER-TOKENIZER-004
        """

        if self.entry_handler is None:
            msg = "Entry entry_handler not given!"
            raise TokenizerError(msg)

        listened_entry_types = set(self.entry_handler.listener.keys())
        unknown_entry_types = listened_entry_types.difference(self._entry_type_pattern.keys())
        if unknown_entry_types:
            msg = "Unknown registered entry type"
            raise TokenizerError(msg)

        entry_type_pattern = dict(item for item in self._entry_type_pattern.items() if item[0] in listened_entry_types)

        for line in stream:
            for entry_type, pattern in entry_type_pattern.items():
                match = pattern.match(line)

                if match:
                    self.entry_handler.entry(entry_type, match.groupdict())
                    if self.echo:
                        sys.stdout.write(line)
