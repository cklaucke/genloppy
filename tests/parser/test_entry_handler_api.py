import pytest

from genloppy.parser.entry_handler_api import EntryHandlerInterface


def test_01_entry_handler_api():
    """
    Tests the processor API.

    tests: R-ENTRY-HANDLER-API-001
    tests: R-ENTRY-HANDLER-API-002
    tests: R-ENTRY-HANDLER-API-003
    tests: R-ENTRY-HANDLER-API-004
    """
    assert hasattr(EntryHandlerInterface, "register_listener")
    assert hasattr(EntryHandlerInterface, "listener")
    assert hasattr(EntryHandlerInterface, "entry")

    i = EntryHandlerInterface()

    with pytest.raises(NotImplementedError):
        i.register_listener(None, None)

    with pytest.raises(NotImplementedError):
        i.listener()

    with pytest.raises(NotImplementedError):
        i.entry(None, None)
