__author__ = "cklaucke"


from genloppy.processor import Interface

import nose.tools


def test_01_processor_interface():
    """
    Tests the processor API.

    tests: R-PROCESSOR-API-001
    tests: R-PROCESSOR-API-002
    tests: R-PROCESSOR-API-003
    tests: R-PROCESSOR-API-004
    """
    i = Interface()

    for method in [i.callbacks,
                   i.pre_process,
                   i.post_process]:
        with nose.tools.assert_raises(NotImplementedError):
            method()
