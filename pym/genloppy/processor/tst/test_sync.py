from genloppy.processor.sync import Sync
from genloppy.processor.base import BaseOutput

import nose.tools
from unittest.mock import MagicMock, call


def test_01_base_output_subclass():
    """Tests that sync processor is BaseOutput subclass.
    tests: R-PROCESSOR-SYNC-001"""
    nose.tools.assert_true(issubclass(Sync, BaseOutput))


def test_02_pre_processing():
    """Tests that sync processor calls message with the expected pre-processing text.
    test: R-PROCESSOR-SYNC-002"""
    m = MagicMock()
    sync = Sync(output=m)
    sync.pre_process()
    nose.tools.assert_equal(m.method_calls, [call.message("")])


def test_03_callback_added():
    """Tests that sync processor added 'process' to callbacks for 'sync'.
    tests: R-PROCESSOR-SYNC-003"""
    sync = Sync(output=None)
    nose.tools.assert_dict_equal(sync.callbacks, dict(sync=sync.process))


def test_04_post_processing():
    """Tests that sync processor calls message with the expected post-processing text.
    test: R-PROCESSOR-SYNC-004"""
    m = MagicMock()
    sync = Sync(output=m)
    sync.post_process()
    nose.tools.assert_equal(m.method_calls, [call.message("")])


def test_05_processing():
    """Tests that sync processor calls sync_item with the expected parameters.
    test: R-PROCESSOR-SYNC-005"""
    m = MagicMock()
    sync = Sync(output=m)
    info = dict(timestamp=1337)
    sync.process(info)
    nose.tools.assert_equal(m.method_calls, [call.sync_item(info["timestamp"])])
