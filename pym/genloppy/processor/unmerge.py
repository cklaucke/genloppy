from genloppy.processor.base import BaseOutput


class Unmerge(BaseOutput):
    """List unmerge processor implementation
    realizes: R-PROCESSOR-UNMERGE-001
    realizes: R-PROCESSOR-UNMERGE-002
    """
    HEADER = " * packages unmerged:\n"

    def __init__(self, **kwargs):
        """Adds callback for 'unmerge'.
        realizes: R-PROCESSOR-UNMERGE-003"""
        super().__init__(**kwargs)
        self._add_callbacks(unmerge=self.process)

    def process(self, item):
        """Prints unmerge information.
        realizes: R-PROCESSOR-UNMERGE-004"""
        self.output.unmerge_item(item["timestamp"], item["name"], item["version"])
