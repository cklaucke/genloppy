from collections import defaultdict


class EntryHandler:
    """
    Handles events and allows registering listeners.

    realizes: R-PARSER-ENTRY-HANDLER-001
    """

    def __init__(self, entry_types):
        self.listener = defaultdict(list)
        self._entry_types = list(entry_types)

    def register_listener(self, callback, entry_type=None):
        """Registers a listener for entry events

        :param callback: a callable taking a properties dictionary
        :param entry_type: an entry type to register for; if None register for all available entry types

        realizes: R-PARSER-ENTRY-HANDLER-003
        """
        if entry_type is None:
            for known_entry_type in self._entry_types:
                self.listener[known_entry_type].append(callback)
        elif entry_type in self._entry_types:
            self.listener[entry_type].append(callback)
        else:
            raise RuntimeError("Cannot register listener '{}' to unknown entry type '{}'."
                               .format(callback, entry_type))

    def entry(self, entry_type, properties):
        """Callback for the parser.

        :param entry_type: type of the entry event
        :param properties: parsed key-value pairs of the entry

        realizes: R-PARSER-ENTRY-HANDLER-004
        """
        for listener in self.listener[entry_type]:
            listener(properties)
