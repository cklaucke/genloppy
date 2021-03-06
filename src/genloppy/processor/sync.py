from genloppy.processor.base import BaseOutput


class Sync(BaseOutput):
    """List sync processor implementation
    realizes: R-PROCESSOR-SYNC-001
    realizes: R-PROCESSOR-SYNC-002
    """

    def __init__(self, **kwargs):
        """Adds callback for 'sync'.
        realizes: R-PROCESSOR-SYNC-003"""
        super().__init__(callbacks={"sync": self.process}, **kwargs)

    def process(self, properties):
        """Prints sync information.
        realizes: R-PROCESSOR-SYNC-004"""
        self.output.sync_item(properties["timestamp"])
