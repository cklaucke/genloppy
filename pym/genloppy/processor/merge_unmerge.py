from genloppy.processor.base import BaseOutput
from genloppy.processor.merge import Merge
from genloppy.processor.unmerge import Unmerge


class MergeUnmerge(BaseOutput):
    """List merge and unmerge processor implementation
    realizes: R-PROCESSOR-MERGE-UNMERGE-001
    """
    HEADER = " * packages merged and unmerged:\n"
    TRAILER = ""

    def __init__(self, **kwargs):
        """Adds callbacks from 'merge' and 'unmerge'.
        realizes: R-PROCESSOR-MERGE-UNMERGE-003"""
        super().__init__(**kwargs)
        self._merge = Merge(**kwargs)
        self._unmerge = Unmerge(**kwargs)
        self._add_callbacks(**self._merge.callbacks)
        self._add_callbacks(**self._unmerge.callbacks)

    def pre_process(self):
        """Prints header.
        realizes: R-PROCESSOR-MERGE-UNMERGE-002"""
        self.output.message(self.HEADER)

    def post_process(self):
        """Prints trailer.
        realizes: R-PROCESSOR-MERGE-UNMERGE-004"""
        self.output.message(self.TRAILER)
