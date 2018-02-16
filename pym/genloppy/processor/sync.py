from genloppy.processor.base import BaseOutput


class Sync(BaseOutput):
    """List sync processor implementation
    realizes: R-PROCESSOR-SYNC-001
    """
    HEADER = ""
    TRAILER = ""

    def __init__(self, **kwargs):
        """Adds callback for 'sync'.
        realizes: R-PROCESSOR-SYNC-003"""
        super().__init__(**kwargs)
        self._add_callbacks(sync=self.process)

    def pre_process(self):
        """Prints header.
        realizes: R-PROCESSOR-SYNC-002"""
        self.output.message(self.HEADER)

    def process(self, item):
        """Prints sync information.
        realizes: R-PROCESSOR-SYNC-005"""
        self.output.sync_item(item["timestamp"])

    def post_process(self):
        """Prints trailer.
        realizes: R-PROCESSOR-SYNC-004"""
        self.output.message(self.TRAILER)
