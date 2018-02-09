from genloppy.processor.base import Base

import nose.tools


def test_01_base_processor():
    """
    Tests the processor API of the base processor.

    tests: R-PROCESSOR-BASE-001
    tests: R-PROCESSOR-BASE-002
    tests: R-PROCESSOR-BASE-003
    tests: R-PROCESSOR-BASE-004
    """
    b = Base()

    nose.tools.assert_dict_equal(b.callbacks, {})

    def bar():
        pass

    b._add_callbacks(foo=bar)
    nose.tools.assert_dict_equal(b.callbacks, dict(foo=bar))

    b.pre_process()
    b.post_process()
