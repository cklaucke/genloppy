from genloppy.processor.base import BaseOutput
from genloppy.processor.merge import Merge
from genloppy.processor.unmerge import Unmerge


class MergeUnmerge(BaseOutput):
    """List merge and unmerge processor implementation
    realizes: R-PROCESSOR-MERGE-UNMERGE-001
    realizes: R-PROCESSOR-MERGE-UNMERGE-002
    """
    HEADER = " * packages merged and unmerged:\n"

    def __init__(self, **kwargs):
        """Adds callbacks from 'merge' and 'unmerge'.
        realizes: R-PROCESSOR-MERGE-UNMERGE-003"""
        super().__init__(**kwargs)
        self._merge = Merge(**kwargs)
        self._unmerge = Unmerge(**kwargs)
        self._add_callbacks(**self._merge.callbacks)
        self._add_callbacks(**self._unmerge.callbacks)
