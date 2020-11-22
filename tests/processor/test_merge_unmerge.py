from unittest.mock import MagicMock
from unittest.mock import call

from genloppy.processor.base import BaseOutput
from genloppy.processor.merge_unmerge import MergeUnmerge


def test_01a_base_output_subclass():
    """Tests that merge and unmerge processor is BaseOutput subclass.
    tests: R-PROCESSOR-MERGE-UNMERGE-001"""
    assert issubclass(MergeUnmerge, BaseOutput)


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
    # just test that callbacks are added, do not test behavior of other processors
    assert len(merge_unmerge.callbacks) > 0


def test_04_post_processing():
    """Tests that merge and unmerge processor calls message with the expected post-processing text.
    test: R-PROCESSOR-MERGE-UNMERGE-002"""
    m = MagicMock()
    merge_unmerge = MergeUnmerge(output=m)
    merge_unmerge.post_process()
    assert m.method_calls == [call.message("")]
