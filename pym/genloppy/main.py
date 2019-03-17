#!/usr/bin/env python3
import sys

from genloppy.configurator import CommandLine as CommandLineConfigurator
from genloppy.output import Output
from genloppy.parser.emerge_log import EmergeLogParser
from genloppy.parser.entry_handler import EntryHandler
from genloppy.processor import ProcessorFactory

DEFAULT_ELOG_FILE = "/var/log/emerge.log"


class Main:
    """
    Provides main function

    realizes: R-MAIN-001
    """

    def __init__(self, configurator, processor_factory, elog_parser, entry_handler, output):
        self.configurator = configurator
        self.processor_factory = processor_factory
        self.elog_parser = elog_parser
        self.entry_handler = entry_handler
        self.output = output
        self.processor = None

    def _create_processor(self):
        processor_configuration = dict(self.configurator.processor_configuration)
        processor_name = processor_configuration.pop("name")
        self.processor = self.processor_factory.create(processor_name, output=self.output, **processor_configuration)

    def _setup_parser(self):
        parser_configuration = dict(self.configurator.parser_configuration)
        parser_configuration.pop("file_names")
        self.elog_parser.configure(**parser_configuration)
        self.elog_parser.handler = self.entry_handler
        for entry_type, callback in self.processor.callbacks.items():
            self.entry_handler.register_listener(callback, entry_type)

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

        allowed_parser_configuration = dict(file_names=None,
                                            package_names=None,
                                            search_reg_exps=None,
                                            case_sensitive=False,
                                            dates=None)
        allowed_processor_configuration = dict(query=False)
        allowed_output_configuration = dict(utc=False,
                                            color=False)

        config_compare(self.configurator.parser_configuration, allowed_parser_configuration)
        config_compare(self.configurator.processor_configuration, allowed_processor_configuration)
        config_compare(self.configurator.output_configuration, allowed_output_configuration)

    def run(self):
        """
        Obtains the desired processor, subscribes, pre-processes, invokes the parser and
        post-processes.

        realizes: R-MAIN-002
        """
        self.configurator.parse_arguments()
        self._config_feature_check()
        self._create_processor()
        self._setup_parser()
        self._configure_output()

        self.processor.pre_process()
        with open(DEFAULT_ELOG_FILE) as f:
            self.elog_parser.parse(f)
        self.processor.post_process()


def main(argv):
    runtime = dict(
        configurator=CommandLineConfigurator(argv[1:]),
        processor_factory=ProcessorFactory(),
        elog_parser=EmergeLogParser(),
        entry_handler=None,
        output=Output()
    )
    entry_types = runtime["elog_parser"].entry_types
    runtime.update(entry_handler=EntryHandler(entry_types=entry_types))
    m = Main(**runtime)
    m.run()


if __name__ == "__main__":
    main(sys.argv)  # pragma: no cover
