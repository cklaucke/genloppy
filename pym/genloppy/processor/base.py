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
