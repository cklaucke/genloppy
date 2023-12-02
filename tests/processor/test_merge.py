from unittest.mock import MagicMock
from unittest.mock import call

from genloppy.processor.base import BaseOutput
from genloppy.processor.merge import Merge


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
    assert merge.callbacks == dict(merge_end=merge.process)


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
    info = dict(timestamp=1337, atom_base="cat/package", atom_version="3.2.1")
    merge.process(info)
    assert m.method_calls == [call.merge_item(info["timestamp"], info["atom_base"], info["atom_version"])]
