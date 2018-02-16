from genloppy.processor.unmerge import Unmerge
from genloppy.processor.base import BaseOutput

import nose.tools
from unittest.mock import MagicMock, call


def test_01_base_output_subclass():
    """Tests that unmerge processor is BaseOutput subclass.
    tests: R-PROCESSOR-UNMERGE-001"""
    nose.tools.assert_true(issubclass(Unmerge, BaseOutput))


def test_02_pre_processing():
    """Tests that unmerge processor calls message with the expected pre-processing text.
    test: R-PROCESSOR-UNMERGE-002"""
    m = MagicMock()
    unmerge = Unmerge(output=m)
    unmerge.pre_process()
    nose.tools.assert_equal(m.method_calls, [call.message(" * packages unmerged:\n")])


def test_03_callback_added():
    """Tests that unmerge processor added 'process' to callbacks for 'unmerge'.
    tests: R-PROCESSOR-UNMERGE-003"""
    unmerge = Unmerge(output=None)
    nose.tools.assert_dict_equal(unmerge.callbacks, dict(unmerge=unmerge.process))


def test_04_post_processing():
    """Tests that unmerge processor calls message with the expected post-processing text.
    test: R-PROCESSOR-UNMERGE-004"""
    m = MagicMock()
    unmerge = Unmerge(output=m)
    unmerge.post_process()
    nose.tools.assert_equal(m.method_calls, [call.message("")])


def test_05_processing():
    """Tests that unmerge processor calls unmerge_item with the expected parameters.
    test: R-PROCESSOR-UNMERGE-005"""
    m = MagicMock()
    unmerge = Unmerge(output=m)
    info = dict(timestamp=1337, name="cat/package", version="3.2.1")
    unmerge.process(info)
    nose.tools.assert_equal(m.method_calls, [call.unmerge_item(info["timestamp"],
                                                               info["name"],
                                                               info["version"])])

