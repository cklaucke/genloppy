import pytest

from genloppy.parser.entry_handler import EntryHandler


def test_01a_registering_unknown_entry_type_raises():
    """
    Tests that an exception is raised if trying to register for an unknown entry type.

    tests: R-PARSER-ENTRY-HANDLER-001
    tests: R-PARSER-ENTRY-HANDLER-002
    tests: R-PARSER-ENTRY-HANDLER-003
    """
    eh = EntryHandler([])

    with pytest.raises(RuntimeError):
        eh.register_listener(lambda x: x, "void")


def test_01b_register_listener_succeeds():
    """
    Tests that registering a listener succeeds.

    tests: R-PARSER-ENTRY-HANDLER-001
    tests: R-PARSER-ENTRY-HANDLER-002
    tests: R-PARSER-ENTRY-HANDLER-003
    """
    eh = EntryHandler(["foo", "bar"])

    cb = lambda x: x
    eh.register_listener(cb, "foo")
    assert cb in eh.listener["foo"]

    cb1 = lambda x: x
    eh.register_listener(cb1)
    assert cb1 in eh.listener["foo"]
    assert cb1 in eh.listener["bar"]


def test_02_listener_gets_called():
    """
    Tests that the registered listener gets called.

    tests: R-PARSER-ENTRY-HANDLER-004
    """

    class EntryCapture:
        def __init__(self):
            self.calls = 0
            self.properties = None

        def capture(self, properties):
            self.calls += 1
            self.properties = properties

    ec = EntryCapture()
    eh = EntryHandler(["foo", "bar"])
    eh.register_listener(ec.capture, "foo")

    properties = dict(start=1337, stop="infinite")

    eh.entry("bar", dict(one=1, two="2"))
    assert ec.calls == 0
    assert ec.properties == None

    eh.entry("foo", properties)
    assert ec.calls == 1
    assert ec.properties == properties
