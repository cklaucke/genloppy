from unittest.mock import MagicMock
from unittest.mock import call

import genloppy.parser.filter


def test_01_filter_factory_function():
    """
    Tests that the filter factory function creates filter instances.

    tests: R-FILTER-001
    """
    m = MagicMock()
    genloppy.parser.filter.FILTER = {"mock": m}
    genloppy.parser.filter.create("mock", ["param1", "param2"])

    assert m.call_args == call(["param1", "param2"])

    genloppy.parser.filter.create("mock", ["param1", "param2"], extra=True)

    assert m.call_args == call(["param1", "param2"], extra=True)
