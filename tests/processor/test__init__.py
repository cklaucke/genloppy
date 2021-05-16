from unittest.mock import MagicMock
from unittest.mock import call

import genloppy.processor


def test_01_processor_factory_function():
    """
    Tests that the processor factory function creates processor instances.

    tests: R-PROCESSOR-001
    """
    m = MagicMock()
    genloppy.processor.PROCESSORS = {"mock": m}
    genloppy.processor.create("mock")

    assert m.call_args == call()

    genloppy.processor.create("mock", extra=True)

    assert m.call_args == call(extra=True)
