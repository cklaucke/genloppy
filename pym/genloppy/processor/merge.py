from genloppy.processor.base import BaseOutput


class Merge(BaseOutput):
    """List merge processor implementation
    realizes: R-PROCESSOR-MERGE-001
    realizes: R-PROCESSOR-MERGE-002
    """
    HEADER = " * packages merged:\n"

    def __init__(self, **kwargs):
        """Adds callback for 'merge'.
        realizes: R-PROCESSOR-MERGE-003"""
        super().__init__(**kwargs)
        self._add_callbacks(merge=self.process)

    def process(self, item):
        """Prints merge information.
        realizes: R-PROCESSOR-MERGE-004"""
        self.output.merge_item(item["timestamp_end"], item["name"], item["version"])
