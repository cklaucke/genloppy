import genloppy.processor

from unittest.mock import MagicMock


def test_01_processor_factory():
    """
    Tests that the processor factory creates processor instances.

    tests: R-PROCESSOR-001
    """

    genloppy.processor.PROCESSORS = {"mock": MagicMock}
    pf = genloppy.processor.ProcessorFactory()
    processor = pf.create("mock")

    assert isinstance(processor, MagicMock)
