from genloppy.processor.base import Base, BaseOutput


def test_01_base_processor():
    """
    Tests the processor API of the base processor.

    tests: R-PROCESSOR-BASE-001
    tests: R-PROCESSOR-BASE-002
    tests: R-PROCESSOR-BASE-003
    tests: R-PROCESSOR-BASE-004
    """

    def bar():
        pass

    b = Base(callbacks={"foo": bar})

    assert b.callbacks == {"foo": bar}
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


def test_03_base_output_processor_default_impl():
    """
    Tests the default implementation of the base processor.
    tests: R-PROCESSOR-BASE-OUTPUT-002"""

    class MockOutput:
        def __init__(self):
            self.messages = []

        def message(self, msg):
            self.messages.append(msg)

    m = MockOutput()
    b = BaseOutput(output=m)
    b.pre_process()
    b.post_process()

    assert m.messages == ["", ""]
