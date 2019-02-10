import genloppy.main
from genloppy.processor.base import BaseOutput as ProcessorBaseOutput
from genloppy.output import Interface

from os import unlink
from tempfile import NamedTemporaryFile
from unittest.mock import patch, call


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
            self._callbacks.update(merge=self.process)
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
            self.subscriptions = []
            self.parse_called_count = 0
            self.content = None

        def configure(self, **kwargs):
            self.kwargs = kwargs

        def subscribe(self, callback, mode):
            self.subscriptions.append((callback, mode))

        def parse(self, f):
            self.parse_called_count += 1
            self.content = f.read()
            for callback, _ in self.subscriptions:
                callback(None)

    class MockOutput(Interface):
        def configure(self, **kwargs):
            pass

    assert genloppy.main.DEFAULT_ELOG_FILE == "/var/log/emerge.log"

    mock_configurator = MockConfigurator()
    mock_processor_factory = MockProcessorFactory()
    mock_elog_parser = MockEmergeLogParser()
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
                               output=mock_output)
        m.run()
    finally:
        if temp_file:
            unlink(temp_file.name)

    assert mock_configurator.parse_arguments_calls == 1

    assert mock_elog_parser.kwargs == dict(filter="all")
    assert len(mock_elog_parser.subscriptions) == 1
    assert mock_elog_parser.parse_called_count == 1
    assert mock_elog_parser.content == content

    assert len(mock_processor_factory.created_processors) == 1
    assert mock_processor_factory.created_processors[0][0] == "mock"

    mock_processor = mock_processor_factory.created_processors[0][1]
    assert mock_processor.kwargs == dict(output=mock_output, feature="42")
    assert mock_processor.call_order == ["pre_process", "process(None)", "post_process"]


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
