from os import unlink
from tempfile import NamedTemporaryFile
from unittest.mock import call
from unittest.mock import patch

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
            self._parser_configuration = dict(file_names=None)
            self._filter_configuration = dict(package_names=["cat/package"])
            self._filter_extra_configuration = dict(extra=True)
            self._processor_configuration = dict(name="mock", feature="42")
            self._output_configuration = dict(format="special")
            self.parse_arguments_calls = 0

        def parse_arguments(self):
            self.parse_arguments_calls += 1

        @property
        def parser_configuration(self):
            return self._parser_configuration

        @property
        def filter_configuration(self):
            return self._filter_configuration

        @property
        def filter_extra_configuration(self):
            return self._filter_extra_configuration

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

    class MockTokenizer:
        def __init__(self, handler):
            self.kwargs = None
            self._handler = handler
            self.parse_called_count = 0
            self.content = None

        def configure(self, **kwargs):
            self.kwargs = kwargs

        @property
        def entry_handler(self):
            return self._handler

        @entry_handler.setter
        def entry_handler(self, handler):
            self._handler = handler

        def tokenize(self, f):
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

    genloppy.processor.PROCESSORS = {"mock": MockProcessor}
    mock_configurator = MockConfigurator()
    mock_entry_handler = MockEntryHandler()
    mock_elog_parser = MockTokenizer(mock_entry_handler)
    mock_output = MockOutput()

    content = "1337\nalpha\n"
    temp_file = None
    try:
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(content.encode())
        temp_file.close()
        genloppy.main.DEFAULT_ELOG_FILE = temp_file.name
        m = genloppy.main.Main(configurator=mock_configurator,
                               elog_tokenizer=mock_elog_parser,
                               output=mock_output)
        m.run()
    finally:
        if temp_file:
            unlink(temp_file.name)

    # test that parse_arguments() is exactly called once
    assert mock_configurator.parse_arguments_calls == 1

    mock_processor = m.processor
    # test that processor_configuration is forwarded correctly
    assert mock_processor.kwargs == dict(output=mock_output, feature="42")
    # test that pre_process() and post_process() were called once in that order
    assert mock_processor.call_order == ["pre_process", "post_process"]

    # test that parser_configuration is forwarded correctly
    assert mock_elog_parser.kwargs == dict()
    # test that tokenize() is called exactly once
    assert mock_elog_parser.parse_called_count == 1
    # test that the input stream is forwarded correctly
    assert mock_elog_parser.content == content

    # test that entry entry_handler got exactly one registration
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
