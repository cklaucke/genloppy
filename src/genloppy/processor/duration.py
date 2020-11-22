from genloppy.processor.base import Base


class Duration(Base):
    """Duration processor implementation
    realizes: R-PROCESSOR-DURATION-001
    """

    def __init__(self, callback, **kwargs):
        """Initializes the duration processor taking a callback
        and optional keyword arguments.

        :param callback: the callback to be called after a duration calculation

        realizes: R-PROCESSOR-DURATION-002
        realizes: R-PROCESSOR-DURATION-003
        """
        super().__init__(callbacks={"merge_begin": self.merge_begin,
                                    "merge_end": self.merge_end},
                         **kwargs)
        self.callback = callback
        self.current_merge = None

    def merge_begin(self, properties):
        """Saves the properties of the merge_begin entry

        :param properties: the properties/token of the entry

        realizes: R-PROCESSOR-DURATION-004
        """
        self.current_merge = properties

    def merge_end(self, properties):
        """Determines the merge duration of a matching merge_end entry and calls the callback

        :param properties: the properties/token of the entry

        realizes: R-PROCESSOR-DURATION-005
        """
        if self.current_merge:
            keys = ["atom", "count_m", "count_n"]
            if all(self.current_merge[key] == properties[key] for key in keys):
                duration = int(properties["timestamp"]) - int(self.current_merge["timestamp"])
                self.callback(properties, duration)

        self.current_merge = None
