from genloppy.parser.entry_handler_api import EntryHandlerInterface


class EntryHandlerWrapper(EntryHandlerInterface):
    """
    Handles events and allows registering listeners.

    realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-001
    """

    def __init__(self):
        self.entry_handler = None

    def __call__(self, entry_handler):
        """Wraps the entry handler and returns the wrapper.

        :param entry_handler: the entry handler to wrap
        :return the wrapper
        realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-002
        """
        self.entry_handler = entry_handler
        return self

    def register_listener(self, callback, entry_type):
        """Registers a listener for entry events

        :param callback: a callable taking a properties dictionary
        :param entry_type: an entry type to register for

        realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-003
        """
        self.entry_handler.register_listener(callback, entry_type)

    @property
    def listener(self):
        """Gets the registered listeners.

        :return: the registered listeners

        realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-004
        """
        return self.entry_handler.listener

    def entry(self, entry_type, properties):
        """Callback for entry events.

        :param entry_type: type of the entry event
        :param properties: parsed key-value pairs of the entry

        realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-006
        """
        if self.test(properties):
            self.entry_handler.entry(entry_type, properties)

    def test(self, properties):
        """Tests whether the event shall be used or not.

        :param properties: the events key-value pairs

        realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-005
        """
        raise NotImplementedError
