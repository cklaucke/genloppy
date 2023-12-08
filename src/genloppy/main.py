#!/usr/bin/env python3
import dataclasses
import signal
import sys
from dataclasses import dataclass
from functools import reduce

from genloppy import processor
from genloppy.configurator import CommandLine as CommandLineConfigurator
from genloppy.configurator import Configuration
from genloppy.log_files import LogFiles
from genloppy.output import Interface as OutputInterface
from genloppy.output import Output
from genloppy.parser import filter as parser_filter
from genloppy.parser.entry_handler import EntryHandler
from genloppy.parser.pms import EMERGE_LOG_ENTRY_TYPES
from genloppy.parser.tokenizer import Tokenizer
from genloppy.portage_configuration import PortageConfigurationError, get_default_emerge_log_file


@dataclass(frozen=True)
class RuntimeConfiguration:
    configuration: Configuration
    elog_tokenizer: Tokenizer
    output: OutputInterface


class Main:
    """
    Provides main function

    realizes: R-MAIN-001
    """

    def __init__(self, runtime_configuration: RuntimeConfiguration):
        self.configuration = runtime_configuration.configuration
        self.elog_tokenizer = runtime_configuration.elog_tokenizer
        self.output = runtime_configuration.output
        self.processor: processor.Interface | None = None

    def _create_processor(self):
        processor_configuration = dataclasses.asdict(self.configuration.processor)
        processor_name = processor_configuration.pop("name")
        self.processor = processor.create(processor_name, output=self.output, **processor_configuration)

    def _setup_entry_handler(self, entry_handler):
        for entry_type, callback in self.processor.callbacks.items():
            entry_handler.register_listener(callback, entry_type)

        extra_config = dataclasses.asdict(self.configuration.filter_extra)
        filter_config = dataclasses.asdict(self.configuration.filter)
        filters = (parser_filter.create(k, v, **extra_config) for k, v in filter_config.items() if v)
        entry_handler = reduce(lambda _entry_handler, _filter: _filter(_entry_handler), filters, entry_handler)
        return entry_handler

    def _setup_tokenizer(self):
        parser_configuration = dataclasses.asdict(self.configuration.parser)
        parser_configuration.pop("file_names")
        self.elog_tokenizer.configure(**parser_configuration)
        self.elog_tokenizer.entry_handler = self._setup_entry_handler(self.elog_tokenizer.entry_handler)

    def _configure_output(self):
        self.output.configure(**dataclasses.asdict(self.configuration.output))

    def _get_log_files(self):
        """Retrieves the log file names or tries to get the default emerge log file name if no log files were given.

        realizes: R-LOG-FILES-002"""
        file_names = self.configuration.parser.file_names
        if not file_names:
            try:
                file_names = [get_default_emerge_log_file()]
            except PortageConfigurationError as exc:
                raise RuntimeError(
                    "Could not determine path to default emerge log file. Please specify the path at the command line."
                ) from exc
        return file_names

    def _config_feature_check(self):
        """Checks for configuration feature availability."""

        messages = []
        if self.configuration.filter.dates is not None:
            messages.append("limitation of log entries by date")
        if self.configuration.processor.query:
            messages.append("querying of gentoo.linuxhowtos.org database")
        if self.configuration.output.utc:
            messages.append("setting the display time format to GMT/UTC")
        if self.configuration.output.color:
            messages.append("colored output (try to disable colored output)")

        if messages:
            raise NotImplementedError("Sorry, the following features are not implemented yet: " + "\n".join(messages))

    def run(self):
        """
        Obtains the desired processor, sets up tokenizer, pre-processes, invokes the tokenizer and
        post-processes.

        realizes: R-MAIN-002
        """
        self._config_feature_check()
        self._create_processor()
        self._setup_tokenizer()
        self._configure_output()

        self.processor.pre_process()
        for f in LogFiles(self._get_log_files()):
            self.elog_tokenizer.tokenize(f)
        self.processor.post_process()


def main(argv=None):
    if argv is None:  # pragma: no cover
        argv = sys.argv

    configurator = CommandLineConfigurator(argv[1:])
    try:
        runtime = RuntimeConfiguration(
            configuration=configurator.parse_arguments(),
            elog_tokenizer=Tokenizer(EMERGE_LOG_ENTRY_TYPES, EntryHandler()),
            output=Output(),
        )
        m = Main(runtime)
        m.run()
    except BaseException as e:
        print(f"Error: {e}", file=sys.stderr)
        configurator.print_help()
        sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # pragma: no cover
    main()  # pragma: no cover
