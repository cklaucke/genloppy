#!/usr/bin/env python3
import signal
import sys
from functools import reduce

from genloppy.configurator import CommandLine as CommandLineConfigurator
from genloppy.output import Output
from genloppy.parser import filter
from genloppy.parser.entry_handler import EntryHandler
from genloppy.parser.pms import EMERGE_LOG_ENTRY_TYPES
from genloppy.parser.tokenizer import Tokenizer
from genloppy.processor import ProcessorFactory

DEFAULT_ELOG_FILE = "/var/log/emerge.log"


class Main:
    """
    Provides main function

    realizes: R-MAIN-001
    """

    def __init__(self, configurator, processor_factory, elog_tokenizer, output):
        self.configurator = configurator
        self.processor_factory = processor_factory
        self.elog_tokenizer = elog_tokenizer
        self.output = output
        self.processor = None

    def _create_processor(self):
        processor_configuration = dict(self.configurator.processor_configuration)
        processor_name = processor_configuration.pop("name")
        self.processor = self.processor_factory.create(processor_name, output=self.output, **processor_configuration)

    def _setup_entry_handler(self, entry_handler):
        for entry_type, callback in self.processor.callbacks.items():
            entry_handler.register_listener(callback, entry_type)

        extra_config = self.configurator.filter_extra_configuration
        filters = (filter.create(k, v, **extra_config) for k, v in self.configurator.filter_configuration.items() if v)
        entry_handler = reduce(lambda entry_handler, filter: filter(entry_handler), filters, entry_handler)
        return entry_handler

    def _setup_tokenizer(self):
        parser_configuration = dict(self.configurator.parser_configuration)
        parser_configuration.pop("file_names")
        self.elog_tokenizer.configure(**parser_configuration)
        self.elog_tokenizer.entry_handler = self._setup_entry_handler(self.elog_tokenizer.entry_handler)

    def _configure_output(self):
        self.output.configure(**self.configurator.output_configuration)

    def _config_feature_check(self):
        """Checks for configuration feature availability."""

        def config_compare(given_configuration, allowed_configuration):
            for key, value in given_configuration.items():
                if key in allowed_configuration.keys() and value is not allowed_configuration[key]:
                    raise NotImplementedError("Sorry, configuration '{}={}' is not implemented, yet. "
                                              "Currently allowed values are '{}'."
                                              .format(key, value, allowed_configuration[key]))  # pragma: no cover

        allowed_parser_configuration = dict(file_names=None)
        allowed_filter_configuration = dict(search_reg_exps=None,
                                            dates=None)
        allowed_processor_configuration = dict(query=False)
        allowed_output_configuration = dict(utc=False,
                                            color=False)

        config_compare(self.configurator.parser_configuration, allowed_parser_configuration)
        config_compare(self.configurator.filter_configuration, allowed_filter_configuration)
        config_compare(self.configurator.processor_configuration, allowed_processor_configuration)
        config_compare(self.configurator.output_configuration, allowed_output_configuration)

    def run(self):
        """
        Obtains the desired processor, sets up tokenizer, pre-processes, invokes the tokenizer and
        post-processes.

        realizes: R-MAIN-002
        """
        self.configurator.parse_arguments()
        self._config_feature_check()
        self._create_processor()
        self._setup_tokenizer()
        self._configure_output()

        self.processor.pre_process()
        with open(DEFAULT_ELOG_FILE) as f:
            self.elog_tokenizer.tokenize(f)
        self.processor.post_process()


def main(argv=sys.argv):
    runtime = dict(
        configurator=CommandLineConfigurator(argv[1:]),
        processor_factory=ProcessorFactory(),
        elog_tokenizer=Tokenizer(EMERGE_LOG_ENTRY_TYPES, EntryHandler()),
        output=Output()
    )
    m = Main(**runtime)
    m.run()


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # pragma: no cover
    main(sys.argv)  # pragma: no cover
