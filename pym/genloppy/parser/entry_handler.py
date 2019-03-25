from collections import defaultdict


class EntryHandler:
    """
    Handles events and allows registering listeners.

    realizes: R-PARSER-ENTRY-HANDLER-001
    """

    def __init__(self):
        self._listener = defaultdict(list)

    def register_listener(self, callback, entry_type):
        """Registers a listener for entry events

        :param callback: a callable taking a properties dictionary
        :param entry_type: an entry type to register for

        realizes: R-PARSER-ENTRY-HANDLER-002
        """
        self._listener[entry_type].append(callback)

    @property
    def listener(self):
        """Gets the registered listeners.

        :return: the registered listeners

        realizes: R-PARSER-ENTRY-HANDLER-003
        """
        return self._listener

    def entry(self, entry_type, properties):
        """Callback for the tokenizer.

        :param entry_type: type of the entry event
        :param properties: parsed key-value pairs of the entry

        realizes: R-PARSER-ENTRY-HANDLER-004
        """
        for listener in self._listener[entry_type]:
            listener(properties)
