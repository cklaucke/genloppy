from genloppy.processor.merge_unmerge import MergeUnmerge, Merge, Unmerge
from genloppy.processor.base import BaseOutput

import nose.tools
from unittest.mock import MagicMock, call


def test_01a_base_output_subclass():
    """Tests that merge and unmerge processor is BaseOutput subclass.
    tests: R-PROCESSOR-MERGE-UNMERGE-001"""
    nose.tools.assert_true(issubclass(MergeUnmerge, BaseOutput))


def test_01b_reuse_merge_and_unmerge_processors():
    """Tests that merge and unmerge processors are reused.
    tests: R-PROCESSOR-MERGE-UNMERGE-001"""
    merge_unmerge = MergeUnmerge(output=None)
    nose.tools.assert_true(isinstance(merge_unmerge._merge, Merge))
    nose.tools.assert_true(isinstance(merge_unmerge._unmerge, Unmerge))


def test_02_pre_processing():
    """Tests that merge and unmerge processor calls message with the expected pre-processing text.
    test: R-PROCESSOR-MERGE-UNMERGE-002"""
    m = MagicMock()
    merge_unmerge = MergeUnmerge(output=m)
    merge_unmerge.pre_process()
    nose.tools.assert_equal(m.method_calls, [call.message(" * packages merged and unmerged:\n")])


def test_03_callback_added():
    """Tests that merge and unmerge processor added callbacks from merge and unmerge processor.
    tests: R-PROCESSOR-MERGE-UNMERGE-003"""
    merge_unmerge = MergeUnmerge(output=None)
    nose.tools.assert_dict_equal(merge_unmerge.callbacks, dict(merge=merge_unmerge._merge.process,
                                                               unmerge=merge_unmerge._unmerge.process))


def test_04_post_processing():
    """Tests that merge and unmerge processor calls message with the expected post-processing text.
    test: R-PROCESSOR-MERGE-UNMERGE-004"""
    m = MagicMock()
    merge_unmerge = MergeUnmerge(output=m)
    merge_unmerge.post_process()
    nose.tools.assert_equal(m.method_calls, [call.message("")])
