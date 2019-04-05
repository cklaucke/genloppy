import pytest

from genloppy.processor import Interface


def test_01_processor_interface():
    """
    Tests the processor API.

    tests: R-PROCESSOR-API-001
    tests: R-PROCESSOR-API-002
    tests: R-PROCESSOR-API-003
    tests: R-PROCESSOR-API-004
    """
    assert hasattr(Interface, "callbacks")
    assert hasattr(Interface, "pre_process")
    assert hasattr(Interface, "post_process")

    i = Interface()

    with pytest.raises(NotImplementedError):
        i.callbacks()
    for method in [i.pre_process, i.post_process]:
        with pytest.raises(NotImplementedError):
            method()
