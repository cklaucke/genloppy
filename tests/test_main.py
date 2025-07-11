from os import unlink
from tempfile import NamedTemporaryFile
from unittest.mock import call, patch

import pytest

import genloppy.main
from genloppy.configurator import (
    Configuration,
    FilterConfiguration,
    FilterExtraConfiguration,
    OutputConfiguration,
    ParserConfiguration,
    ProcessorConfiguration,
)
from genloppy.output import Interface
from genloppy.parser.tokenizer import Tokenizer
from genloppy.portage_configuration import PortageConfigurationError
from genloppy.processor.base import BaseOutput as ProcessorBaseOutput


def _create_configuration(file_names: list[str] | None = None):
    return Configuration(
        parser=ParserConfiguration(file_names=file_names),
        filter=FilterConfiguration(package_names=["cat/package"], dates=None, search_reg_exps=None),
        filter_extra=FilterExtraConfiguration(),
        processor=ProcessorConfiguration(name="mock", active_filter=set()),
        output=OutputConfiguration(color=False),
    )


class _MockProcessor(ProcessorBaseOutput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = kwargs
        self._callbacks.update(merge_begin=self.process)
        self.call_order = []

    def pre_process(self):
        self.call_order.append("pre_process")

    def process(self, item):
        self.call_order.append(f"process({item})")

    def post_process(self):
        self.call_order.append("post_process")


class _MockTokenizer(Tokenizer):
    def __init__(self, handler):
        super().__init__({})  # for completeness' sake
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


class _MockEntryHandler:
    def __init__(self):
        self.registrations = []

    def register_listener(self, callback, entry_type):
        self.registrations.append((callback, entry_type))


class _MockOutput(Interface):
    def __init__(self):
        self.kwargs = None

    def configure(self, **kwargs):
        self.kwargs = kwargs

    def message(self, message): ...

    def merge_item(self, timestamp, name, version): ...

    def unmerge_item(self, timestamp, name, version): ...

    def sync_item(self, timestamp): ...

    def merge_time_item(self, timestamp, name, version, duration): ...


def test_01_main_execution():
    """
    Tests main class execution.

    tests: R-MAIN-002
    """

    genloppy.processor.PROCESSORS = {"mock": _MockProcessor}
    mock_entry_handler = _MockEntryHandler()
    mock_elog_parser = _MockTokenizer(mock_entry_handler)
    mock_output = _MockOutput()

    content = "1337:\n1338: alpha\n"
    temp_file = None
    try:
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(content.encode())

        rc = genloppy.main.RuntimeConfiguration(
            configuration=_create_configuration([temp_file.name]),
            elog_tokenizer=mock_elog_parser,
            output=mock_output,
        )
        m = genloppy.main.Main(rc)
        m.run()
    finally:
        if temp_file is not None:
            unlink(temp_file.name)

    mock_processor = m.processor
    assert mock_processor is not None  # needed to get type right
    assert isinstance(mock_processor, _MockProcessor)  # needed to get type right
    # test that processor_configuration is forwarded correctly
    assert mock_processor.kwargs == {"output": mock_output, "query": False, "active_filter": set()}
    # test that pre_process() and post_process() were called once in that order
    assert mock_processor.call_order == ["pre_process", "post_process"]

    # test that parser_configuration is forwarded correctly
    assert mock_elog_parser.kwargs == {}
    # test that tokenize() is called exactly once
    assert mock_elog_parser.parse_called_count == 1
    # test that the input stream is forwarded correctly
    assert mock_elog_parser.content == content

    # test that entry entry_handler got exactly one registration
    assert len(mock_entry_handler.registrations) == 1
    # test that process of mock processor was registered
    assert mock_entry_handler.registrations[0][0] == mock_processor.process

    # test that output_configuration is forwarded correctly
    assert mock_output.kwargs == {"color": False, "utc": False}

    rc = genloppy.main.RuntimeConfiguration(
        configuration=_create_configuration(),
        elog_tokenizer=mock_elog_parser,
        output=mock_output,
    )
    m = genloppy.main.Main(rc)
    with patch("genloppy.main.get_default_emerge_log_file") as default_log_file_mock:
        default_log_file_mock.side_effect = PortageConfigurationError
        with pytest.raises(RuntimeError) as exception:
            m.run()

    assert exception.value.args[0] == (
        "Could not determine path to default emerge log file. Please specify the path at the command line."
    )


def test_02_main_function():
    """
    Tests the main function.

    tests: R-MAIN-001
    """

    # mocks configurator to avoid validation errors
    with patch("genloppy.main.CommandLineConfigurator"), patch("genloppy.main.Main") as mock:
        # pass empty list to avoid usage of sys.argv
        genloppy.main.main([])
        assert len(mock.mock_calls) == 2
        assert mock.mock_calls[0][0] == ""
        assert mock.mock_calls[1] == call().run()


def test_03_main_function(capsys):
    """Integration test. Test the main function when no arguments are given."""

    with pytest.raises(SystemExit):
        # pass empty list to avoid usage of sys.argv
        genloppy.main.main([])

    captured = capsys.readouterr()
    assert captured.err == (
        "Error: \"At least one sub-command argument (one of '-c', '-l', '-i', '-p', '-r'"
        ", '-t', '-u' or '-v') needed.\"\n"
    )
