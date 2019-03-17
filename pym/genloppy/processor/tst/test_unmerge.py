from unittest.mock import MagicMock, call

from genloppy.processor.base import BaseOutput
from genloppy.processor.unmerge import Unmerge


def test_01_base_output_subclass():
    """Tests that unmerge processor is BaseOutput subclass.
    tests: R-PROCESSOR-UNMERGE-001"""
    assert issubclass(Unmerge, BaseOutput)


def test_02_pre_processing():
    """Tests that unmerge processor calls message with the expected pre-processing text.
    test: R-PROCESSOR-UNMERGE-002"""
    m = MagicMock()
    unmerge = Unmerge(output=m)
    unmerge.pre_process()
    assert m.method_calls == [call.message(" * packages unmerged:\n")]


def test_03_callback_added():
    """Tests that unmerge processor added 'process' to callbacks for 'unmerge'.
    tests: R-PROCESSOR-UNMERGE-003"""
    unmerge = Unmerge(output=None)
    assert unmerge.callbacks == dict(unmerge=unmerge.process)


def test_04_post_processing():
    """Tests that unmerge processor calls message with the expected post-processing text.
    test: R-PROCESSOR-UNMERGE-002"""
    m = MagicMock()
    unmerge = Unmerge(output=m)
    unmerge.post_process()
    assert m.method_calls == [call.message("")]


def test_05_processing():
    """Tests that unmerge processor calls unmerge_item with the expected parameters.
    test: R-PROCESSOR-UNMERGE-004"""
    m = MagicMock()
    unmerge = Unmerge(output=m)
    info = dict(timestamp=1337, atom_base="cat/package", atom_version="3.2.1")
    unmerge.process(info)
    assert m.method_calls == [call.unmerge_item(info["timestamp"],
                                                info["atom_base"],
                                                info["atom_version"])]
