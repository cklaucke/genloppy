__author__ = "cklaucke"


from genloppy.processor.base import Base


def test_01_base_processor():
    """
    Tests the processor API of the base processor.

    tests: R-PROCESSOR-BASE-001
    tests: R-PROCESSOR-BASE-002
    tests: R-PROCESSOR-BASE-003
    tests: R-PROCESSOR-BASE-004
    """
    b = Base()

    callbacks = b.callbacks
    assert not callbacks
    assert isinstance(callbacks, dict)

    b.pre_process()
    b.post_process()
