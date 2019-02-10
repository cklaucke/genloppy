from genloppy.processor.base import Base, BaseOutput


def test_01_base_processor():
    """
    Tests the processor API of the base processor.

    tests: R-PROCESSOR-BASE-001
    tests: R-PROCESSOR-BASE-002
    tests: R-PROCESSOR-BASE-003
    tests: R-PROCESSOR-BASE-004
    """
    b = Base()

    assert b.callbacks == {}

    def bar():
        pass

    b._add_callbacks(foo=bar)
    assert b.callbacks == dict(foo=bar)

    b.pre_process()
    b.post_process()


def test_02_base_output_processor():
    """
    Tests the processor API of the base processor.
    tests: R-PROCESSOR-BASE-OUTPUT-001"""

    class MockOutput:
        pass

    m = MockOutput()
    b = BaseOutput(output=m)
    assert b.output == m
