from unittest.mock import MagicMock, call, patch

import genloppy.parser.filter


def test_01_filter_factory_function():
    """
    Tests that the filter factory function creates filter instances.

    tests: R-FILTER-001
    """
    m = MagicMock()
    with patch.dict(genloppy.parser.filter.FILTER, {"mock": m}, clear=True):
        genloppy.parser.filter.create("mock", ["param1", "param2"])

    assert m.call_args == call(["param1", "param2"])

    with patch.dict(genloppy.parser.filter.FILTER, {"mock": m}, clear=True):
        genloppy.parser.filter.create("mock", ["param1", "param2"], extra=True)

    assert m.call_args == call(["param1", "param2"], extra=True)
