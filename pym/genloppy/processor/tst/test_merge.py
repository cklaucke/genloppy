from genloppy.processor.merge import Merge
from genloppy.processor.base import BaseOutput

from unittest.mock import MagicMock, call


def test_01_base_output_subclass():
    """Tests that merge processor is BaseOutput subclass.
    tests: R-PROCESSOR-MERGE-001"""
    assert issubclass(Merge, BaseOutput)


def test_02_pre_processing():
    """Tests that merge processor calls message with the expected pre-processing text.
    test: R-PROCESSOR-MERGE-002"""
    m = MagicMock()
    merge = Merge(output=m)
    merge.pre_process()
    assert m.method_calls == [call.message(" * packages merged:\n")]


def test_03_callback_added():
    """Tests that merge processor added 'process' to callbacks for 'merge'.
    tests: R-PROCESSOR-MERGE-003"""
    merge = Merge(output=None)
    assert merge.callbacks == dict(merge=merge.process)


def test_04_post_processing():
    """Tests that merge processor calls message with the expected post-processing text.
    test: R-PROCESSOR-MERGE-002"""
    m = MagicMock()
    merge = Merge(output=m)
    merge.post_process()
    assert m.method_calls == [call.message("")]


def test_05_processing():
    """Tests that merge processor calls merge_item with the expected parameters.
    test: R-PROCESSOR-MERGE-004"""
    m = MagicMock()
    merge = Merge(output=m)
    info = dict(timestamp_end=1337, name="cat/package", version="3.2.1")
    merge.process(info)
    assert m.method_calls == [call.merge_item(info["timestamp_end"],
                                              info["name"],
                                              info["version"])]
