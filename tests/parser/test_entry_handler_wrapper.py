from unittest.mock import MagicMock, call, patch

import pytest

from genloppy.parser.entry_handler_wrapper import EntryHandlerWrapper


def test_01_wrapping():
    """Tests wrapping of an entry handler.

    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-001
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-002
    """
    m = MagicMock()
    wrapper = EntryHandlerWrapper({})
    wrapped_m = wrapper(m)

    assert wrapper == wrapped_m
    assert wrapped_m.entry_handler == m


def test_02_directly_delegated_calls():
    """Tests that register_listener and listener calls are directly delegated to the wrapped entry handler.

    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-001
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-002
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-003
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-004
    """
    m = MagicMock()
    wrapper = EntryHandlerWrapper({})
    wrapper(m)

    wrapper.register_listener(None, None)
    wrapper.listener()

    assert m.method_calls == [call.register_listener(None, None), call.listener()]


def test_03_entry_filter_accept():
    """Tests that entry is accepted if test is True.

    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-001
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-002
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-005
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-006
    """
    m = MagicMock()

    with patch.object(EntryHandlerWrapper, "test", return_value=True) as mock_test:
        wrapper = EntryHandlerWrapper({})(m)
        wrapper.entry(None, None)

    assert m.method_calls == [call.entry(None, None)]
    mock_test.assert_called_once_with(None)


def test_04_entry_filter_reject():
    """Tests that entry is rejected if test is False.

    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-001
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-002
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-005
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-006
    """
    m = MagicMock()

    with patch.object(EntryHandlerWrapper, "test", return_value=False) as mock_test:
        wrapper = EntryHandlerWrapper({})(m)
        wrapper.entry(None, None)

    assert m.method_calls == []
    mock_test.assert_called_once_with(None)


def test_05_predicate_api():
    """Tests that predicate API os provided.

    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-001
    tests: R-PARSER-ENTRY-HANDLER-WRAPPER-005
    """
    wrapper = EntryHandlerWrapper({})
    assert hasattr(wrapper, "test")

    with pytest.raises(NotImplementedError):
        wrapper.test(None)
