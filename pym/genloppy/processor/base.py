from genloppy.processor.api import Interface as ProcessorInterface


class Base(ProcessorInterface):
    """Base processor implementation

    realizes: R-PROCESSOR-BASE-001
    """
    def __init__(self, **kwargs):
        self._callbacks = {}

    def _add_callbacks(self, **kwargs):
        self._callbacks.update(kwargs)

    @property
    def callbacks(self):
        """Returns a empty dict of modes and associated callbacks to be subscribed.

        realizes: R-PROCESSOR-BASE-003"""
        return self._callbacks

    def pre_process(self):
        """Pre-processes.

        realizes: R-PROCESSOR-BASE-002"""
        pass

    def post_process(self):
        """Post-processes.

        realizes: R-PROCESSOR-BASE-004"""
        pass


class BaseOutput(Base):
    """Implements a base processor that supports output.
    realizes: R-PROCESSOR-BASE-OUTPUT-001"""
    HEADER = ""
    TRAILER = ""

    def __init__(self, output, **kwargs):
        super().__init__(**kwargs)
        self.output = output

    def pre_process(self):
        """Prints header.
        realizes: R-PROCESSOR-BASE-OUTPUT-002"""
        self.output.message(self.HEADER)

    def post_process(self):
        """Prints trailer.
        realizes: R-PROCESSOR-BASE-OUTPUT-003"""
        self.output.message(self.TRAILER)
