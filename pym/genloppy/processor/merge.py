from genloppy.processor.base import BaseOutput


class Merge(BaseOutput):
    """List merge processor implementation
    realizes: R-PROCESSOR-MERGE-001
    """
    HEADER = " * packages merged:\n"
    TRAILER = ""

    def __init__(self, **kwargs):
        """Adds callback for 'merge'.
        realizes: R-PROCESSOR-MERGE-003"""
        super().__init__(**kwargs)
        self._add_callbacks(merge=self.process)

    def pre_process(self):
        """Prints header.
        realizes: R-PROCESSOR-MERGE-002"""
        self.output.message(self.HEADER)

    def process(self, item):
        """Prints merge information.
        realizes: R-PROCESSOR-MERGE-005"""
        self.output.merge_item(item["timestamp_end"], item["name"], item["version"])

    def post_process(self):
        """Prints trailer.
        realizes: R-PROCESSOR-MERGE-004"""
        self.output.message(self.TRAILER)
