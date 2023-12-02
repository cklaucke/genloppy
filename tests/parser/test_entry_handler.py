from genloppy.parser.entry_handler import EntryHandler


def test_01_register_listener_succeeds():
    """
    Tests that registering a listener succeeds.

    tests: R-PARSER-ENTRY-HANDLER-001
    tests: R-PARSER-ENTRY-HANDLER-002
    tests: R-PARSER-ENTRY-HANDLER-003
    """
    eh = EntryHandler()

    def cb():
        pass

    eh.register_listener(cb, "foo")
    assert cb in eh.listener["foo"]

    def cb1():
        pass

    eh.register_listener(cb1, "foo")
    eh.register_listener(cb1, "bar")
    assert cb1 in eh.listener["foo"]
    assert cb1 in eh.listener["bar"]


def test_02_listener_gets_called():
    """
    Tests that the registered listener gets called.

    tests: R-PARSER-ENTRY-HANDLER-001
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
    eh = EntryHandler()
    eh.register_listener(ec.capture, "foo")

    properties = {"start": 1337, "stop": "infinite"}

    eh.entry("bar", {"one": 1, "two": "2"})
    assert ec.calls == 0
    assert ec.properties is None

    eh.entry("foo", properties)
    assert ec.calls == 1
    assert ec.properties == properties
