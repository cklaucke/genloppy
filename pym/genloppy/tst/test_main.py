from os import unlink
from tempfile import NamedTemporaryFile
from unittest.mock import patch, call

import genloppy.main
from genloppy.output import Interface
from genloppy.processor.base import BaseOutput as ProcessorBaseOutput


def test_01_main_execution():
    """
    Tests main class execution.

    tests: R-MAIN-002
    """

    class MockConfigurator:
        def __init__(self):
            self._parser_configuration = dict(filter="all", file_names=None)
            self._processor_configuration = dict(name="mock", feature="42")
            self._output_configuration = dict(format="special")
            self.parse_arguments_calls = 0

        def parse_arguments(self):
            self.parse_arguments_calls += 1

        @property
        def parser_configuration(self):
            return self._parser_configuration

        @property
        def processor_configuration(self):
            return self._processor_configuration

        @property
        def output_configuration(self):
            return self._output_configuration

    class MockProcessor(ProcessorBaseOutput):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.kwargs = kwargs
            self._callbacks.update(merge_begin=self.process)
            self.call_order = []

        def pre_process(self):
            self.call_order.append("pre_process")

        def process(self, item):
            self.call_order.append("process({})".format(item))

        def post_process(self):
            self.call_order.append("post_process")

    class MockProcessorFactory:
        def __init__(self):
            self.created_processors = []

        def create(self, name, **kwargs):
            mp = MockProcessor(**kwargs)
            self.created_processors.append((name, mp))
            return mp

    class MockEmergeLogParser:
        def __init__(self):
            self.kwargs = None
            self._handler = None
            self.parse_called_count = 0
            self.content = None

        def configure(self, **kwargs):
            self.kwargs = kwargs

        @property
        def handler(self):
            return self._handler

        @handler.setter
        def handler(self, handler):
            self._handler = handler

        def parse(self, f):
            self.parse_called_count += 1
            self.content = f.read()

    class MockEntryHandler:
        def __init__(self):
            self.registrations = []

        def register_listener(self, callback, entry_type):
            self.registrations.append((callback, entry_type))

    class MockOutput(Interface):
        def __init__(self):
            self.kwargs = None

        def configure(self, **kwargs):
            self.kwargs = kwargs

    assert genloppy.main.DEFAULT_ELOG_FILE == "/var/log/emerge.log"

    mock_configurator = MockConfigurator()
    mock_processor_factory = MockProcessorFactory()
    mock_elog_parser = MockEmergeLogParser()
    mock_entry_handler = MockEntryHandler()
    mock_output = MockOutput()

    content = "1337\nalpha\n"
    temp_file = None
    try:
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(content.encode())
        temp_file.close()
        genloppy.main.DEFAULT_ELOG_FILE = temp_file.name
        m = genloppy.main.Main(configurator=mock_configurator,
                               processor_factory=mock_processor_factory,
                               elog_parser=mock_elog_parser,
                               entry_handler=mock_entry_handler,
                               output=mock_output)
        m.run()
    finally:
        if temp_file:
            unlink(temp_file.name)

    # test that parse_arguments() is exactly called once
    assert mock_configurator.parse_arguments_calls == 1

    # assert that processor factory created a processor instance
    mock_processor = mock_processor_factory.created_processors[0][1]

    # test that processor_configuration is forwarded correctly
    assert mock_processor.kwargs == dict(output=mock_output, feature="42")
    # test that pre_process() and post_process() were called once in that order
    assert mock_processor.call_order == ["pre_process", "post_process"]

    # test that parser_configuration is forwarded correctly
    assert mock_elog_parser.kwargs == dict(filter="all")
    # test that parse() is called exactly once
    assert mock_elog_parser.parse_called_count == 1
    # test that the input stream is forwarded correctly
    assert mock_elog_parser.content == content
    # test that the entry handler is set correctly
    assert mock_elog_parser.handler == mock_entry_handler

    # test that entry handler got exactly one registration
    assert len(mock_entry_handler.registrations) == 1
    # test that process of mock processor was registered
    assert mock_entry_handler.registrations[0][0] == mock_processor.process

    # test that output_configuration is forwarded correctly
    assert mock_output.kwargs == dict(format="special")


def test_02_main_function():
    """
    Tests the main function.

    tests: R-MAIN-001
    """

    with patch('genloppy.main.Main') as mock:
        genloppy.main.main([])
        assert len(mock.mock_calls) == 2
        assert mock.mock_calls[0][0] == ""
        assert mock.mock_calls[1] == call().run()
