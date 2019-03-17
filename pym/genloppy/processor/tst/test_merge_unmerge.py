from unittest.mock import MagicMock, call

from genloppy.processor.base import BaseOutput
from genloppy.processor.merge_unmerge import MergeUnmerge, Merge, Unmerge


def test_01a_base_output_subclass():
    """Tests that merge and unmerge processor is BaseOutput subclass.
    tests: R-PROCESSOR-MERGE-UNMERGE-001"""
    assert issubclass(MergeUnmerge, BaseOutput)


def test_01b_reuse_merge_and_unmerge_processors():
    """Tests that merge and unmerge processors are reused.
    tests: R-PROCESSOR-MERGE-UNMERGE-001"""
    merge_unmerge = MergeUnmerge(output=None)
    assert isinstance(merge_unmerge._merge, Merge)
    assert isinstance(merge_unmerge._unmerge, Unmerge)


def test_02_pre_processing():
    """Tests that merge and unmerge processor calls message with the expected pre-processing text.
    test: R-PROCESSOR-MERGE-UNMERGE-002"""
    m = MagicMock()
    merge_unmerge = MergeUnmerge(output=m)
    merge_unmerge.pre_process()
    assert m.method_calls == [call.message(" * packages merged and unmerged:\n")]


def test_03_callback_added():
    """Tests that merge and unmerge processor added callbacks from merge and unmerge processor.
    tests: R-PROCESSOR-MERGE-UNMERGE-003"""
    merge_unmerge = MergeUnmerge(output=None)
    assert merge_unmerge.callbacks == dict(merge_end=merge_unmerge._merge.process,
                                           unmerge=merge_unmerge._unmerge.process)


def test_04_post_processing():
    """Tests that merge and unmerge processor calls message with the expected post-processing text.
    test: R-PROCESSOR-MERGE-UNMERGE-002"""
    m = MagicMock()
    merge_unmerge = MergeUnmerge(output=m)
    merge_unmerge.post_process()
    assert m.method_calls == [call.message("")]
