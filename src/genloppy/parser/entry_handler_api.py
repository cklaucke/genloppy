class EntryHandlerInterface:
    """
    Provides the API for handling entry events

    realizes: R-PARSER-ENTRY-HANDLER-API-001
    """

    def register_listener(self, callback, entry_type):
        """Registers a listener for entry events

        :param callback: a callable taking a properties dictionary
        :param entry_type: an entry type to register for

        realizes: R-PARSER-ENTRY-HANDLER-API-002
        """
        raise NotImplementedError

    @property
    def listener(self):
        """Gets the registered listener.

        :return: the registered listener
        """
        raise NotImplementedError

    def entry(self, entry_type, properties):
        """Callback for entry events.

        :param entry_type: type of the entry event
        :param properties: parsed key-value pairs of the entry

        realizes: R-PARSER-ENTRY-HANDLER-API-003
        """
        raise NotImplementedError
