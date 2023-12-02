import argparse
import dataclasses
from dataclasses import dataclass
from typing import Any, Final

import genloppy.processor


@dataclass(frozen=True)
class _CommandLineOptions:
    help: str
    action: str | None = None
    nargs: str | None = None
    const: str | None = None
    default: bool | None = None
    metavar: str | None = None
    dest: str | None = None


@dataclass(frozen=True)
class _CommandLineArgument:
    name_or_flags: tuple[str, ...]
    argparse_options: _CommandLineOptions


@dataclass(frozen=True)
class ProcessorConfiguration:
    name: str
    active_filter: set[str]
    query: bool = False


@dataclass(frozen=True)
class ParserConfiguration:
    file_names: list[str] | None


@dataclass(frozen=True)
class FilterConfiguration:
    package_names: list[str] | None
    search_reg_exps: list[str] | None
    dates: list[str] | None


@dataclass(frozen=True)
class FilterExtraConfiguration:
    case_sensitive: bool = False


@dataclass(frozen=True)
class OutputConfiguration:
    color: bool
    utc: bool = False


@dataclass(frozen=True)
class Configuration:
    processor: ProcessorConfiguration
    parser: ParserConfiguration
    filter: FilterConfiguration
    filter_extra: FilterExtraConfiguration
    output: OutputConfiguration


class CommandLine:
    """Provides the CommandLine Configurator

    realizes: R-CONF-CLI-001"""

    PROCESSORS = genloppy.processor

    # realizes: R-CONF-CLI-002
    # realizes: R-CONF-CLI-003
    # realizes: R-CONF-CLI-004
    # realizes: R-CONF-CLI-005
    ARGUMENTS: Final = (
        # positional
        _CommandLineArgument(
            ("name",),
            _CommandLineOptions(nargs="*", help="package name"),
        ),
        # disguised sub-commands
        _CommandLineArgument(
            ("-c", "--current"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.CURRENT,
                help="prints a merge time estimation for an ongoing merge",
            ),
        ),
        _CommandLineArgument(
            ("-i", "--info"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.INFO,
                help=(
                    "prints a brief summary of the currently installed packages "
                    "(USE, CFLAGS, CXXFLAGS, LDFLAGS, average and total build time)"
                ),
            ),
        ),
        _CommandLineArgument(
            ("-l", "--list"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.MERGE,
                help="prints the history of merges"
            ),
        ),
        _CommandLineArgument(
            ("-p", "--pretend"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.PRETEND,
                help="prints a merge time estimation for the output of emerge -p",
            ),
        ),
        _CommandLineArgument(
            ("-r", "--rsync"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.SYNC,
                help="prints the history of syncs"
            ),
        ),
        _CommandLineArgument(
            ("-t", "--time"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.TIME,
                help="calculates and prints the merge time"
            ),
        ),
        _CommandLineArgument(
            ("-u", "--unmerge"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.UNMERGE,
                help=" which prints the history of unmerges"
            ),
        ),
        _CommandLineArgument(
            ("-v", "--version"),
            _CommandLineOptions(
                dest="sub_commands",
                action="append_const",
                const=PROCESSORS.VERSION,
                help="prints the version information"
            ),
        ),
        # key-value options
        _CommandLineArgument(
            ("--date",),
            _CommandLineOptions(
                action="append",
                help=(
                    "takes a date specification as value. The value of the first occurrence "
                    "of `--date` is taken as start date and the value of the second "
                    "occurrence is taken as end date. The output is limited to log entries "
                    "between start date and end date."
                ),
            ),
        ),
        _CommandLineArgument(
            ("-f",),
            _CommandLineOptions(
                metavar="logfile",
                dest="logfile",
                action="append",
                help="parses the given logfile(s)"
            ),
        ),
        _CommandLineArgument(
            ("-s", "--search"),
            _CommandLineOptions(
                metavar="regex",
                action="append",
                help="takes regular expression(s) as value to be used for package searches"
            ),
        ),
        # flags
        _CommandLineArgument(
            ("-g", "--gmt"),
            _CommandLineOptions(
                dest="utc",
                action="store_true",
                help="sets the display time format to GMT/UTC"
            ),
        ),
        _CommandLineArgument(
            ("-n", "--nocolor"),
            _CommandLineOptions(
                dest="color",
                action="store_false",
                default=True,
                help="disables the colored output"
            ),
        ),
        _CommandLineArgument(
            ("-q",),
            _CommandLineOptions(
                dest="query",
                action="store_true",
                help="queries the gentoo.linuxhowtos.org database if no local emerge was found"
            ),
        ),
        _CommandLineArgument(
            ("-S",),
            _CommandLineOptions(
                dest="case_sensitive",
                action="store_true",
                help="enables case sensitive matching"
            )
        ),
    )

    def __init__(self, arguments):
        self._arguments = arguments
        self._argument_parser = argparse.ArgumentParser()
        self._configure_arguments()

    def _configure_arguments(self):
        """Configures arguments."""

        def _omit_unset_fields(_options: dict[str, Any]) -> dict[str, Any]:
            return {k: v for k, v in _options.items() if v is not None}

        for argument in self.ARGUMENTS:
            options = _omit_unset_fields(dataclasses.asdict(argument.argparse_options))
            self._argument_parser.add_argument(*argument.name_or_flags, **options)

    def _get_processor(self, sub_commands: list[str]) -> str:
        if len(sub_commands) == 1:
            return sub_commands[0]
        elif set(sub_commands) == {self.PROCESSORS.MERGE, self.PROCESSORS.UNMERGE}:
            return self.PROCESSORS.MERGE_UNMERGE
        raise KeyError("Not more than one sub-command allowed at the same time (except '--merge' and '--unmerge').")

    def _validate_arguments(self, parsed_args):
        if not parsed_args.sub_commands:
            raise KeyError(
                "At least one sub-command argument (one of '-c', '-l', '-i', '-p', '-r', '-t', '-u' or '-v') needed.")

        processor_name = self._get_processor(parsed_args.sub_commands)

        if parsed_args.query and processor_name not in self.PROCESSORS.PROCESSORS_ALLOW_QUERY:
            raise KeyError(f"Query flag '-q' not allowed for '{processor_name}'.")

        if (parsed_args.name or parsed_args.search) and processor_name not in self.PROCESSORS.PROCESSORS_ALLOW_NAME:
            raise KeyError(f"Package name(s) or search arguments '-s' not allowed for '{processor_name}'.")

        if not (parsed_args.name or parsed_args.search) and processor_name in self.PROCESSORS.PROCESSORS_REQUIRE_NAME:
            raise KeyError(
                "At least one package name(s) or search arguments '-s' required for '{}'.".format(processor_name)
            )

        date_count = len(parsed_args.date) if parsed_args.date else 0
        if date_count > 2:
            raise KeyError(f"Up to two dates ('--date') may be given. Got {date_count}.")

    def parse_arguments(self) -> Configuration:
        """
        Parses, sanity-checks and evaluates arguments and derives configuration.

        realizes: R-CONF-CLI-006
        """
        parsed_args = self._argument_parser.parse_args(self._arguments)
        self._validate_arguments(parsed_args)

        filter_configuration = FilterConfiguration(
            package_names=parsed_args.name if parsed_args.name else None,
            search_reg_exps=parsed_args.search,
            dates=parsed_args.date,
        )

        return Configuration(
            parser=ParserConfiguration(
                file_names=parsed_args.logfile,
            ),
            filter=filter_configuration,
            processor=ProcessorConfiguration(
                name=self._get_processor(parsed_args.sub_commands),
                query=parsed_args.query,
                active_filter={k for k, v in dataclasses.asdict(filter_configuration).items() if v},
            ),
            filter_extra=FilterExtraConfiguration(
                case_sensitive=parsed_args.case_sensitive,
            ),
            output=OutputConfiguration(
                utc=parsed_args.utc,
                color=parsed_args.color,
            ),
        )

    def print_help(self):
        self._argument_parser.print_help()
