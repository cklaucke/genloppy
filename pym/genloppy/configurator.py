import argparse

import genloppy.processor


class CommandLine:
    """Provides the CommandLine Configurator

    realizes: R-CONF-CLI-001"""
    PROCESSORS = genloppy.processor

    # realizes: R-CONF-CLI-002
    # realizes: R-CONF-CLI-003
    # realizes: R-CONF-CLI-004
    # realizes: R-CONF-CLI-005
    ARGUMENTS = [
        # positional
        (['name'], dict(nargs='*', help='package name')),

        # disguised sub-commands
        (['-c', '--current'], dict(dest="sub_commands", action='append_const',
                                   const=PROCESSORS.CURRENT,
                                   help='prints a merge time estimation for an ongoing merge')),
        (['-i', '--info'], dict(dest="sub_commands", action='append_const',
                                const=PROCESSORS.INFO,
                                help='prints a brief summary of the currently installed packages '
                                     '(USE, CFLAGS, CXXFLAGS, LDFLAGS, average and total build time)')),
        (['-l', '--list'], dict(dest="sub_commands", action='append_const',
                                const=PROCESSORS.MERGE,
                                help='prints the history of merges')),
        (['-p', '--pretend'], dict(dest="sub_commands", action='append_const',
                                   const=PROCESSORS.PRETEND,
                                   help='prints a merge time estimation for the output of emerge -p')),
        (['-r', '--rsync'], dict(dest="sub_commands", action='append_const',
                                 const=PROCESSORS.SYNC,
                                 help='prints the history of syncs')),
        (['-t', '--time'], dict(dest="sub_commands", action='append_const',
                                const=PROCESSORS.TIME,
                                help='calculates and prints the merge time')),
        (['-u', '--unmerge'], dict(dest="sub_commands", action='append_const',
                                   const=PROCESSORS.UNMERGE,
                                   help=' which prints the history of unmerges')),
        (['-v', '--version'], dict(dest="sub_commands", action='append_const',
                                   const=PROCESSORS.VERSION,
                                   help='prints the version information')),

        # key-value options
        (['--date'], dict(action='append',
                          help='takes a date specification as value. The value of the first occurrence '
                               'of `--date` is taken as start date and the value of the second '
                               'occurrence is taken as end date. The output is limited to log entries '
                               'between start date and end date.')),
        (['-f'], dict(metavar='logfile', dest='logfile', action='append',
                      help='parses the given logfile(s)')),
        (['-s', '--search'], dict(metavar='regex', action='append',
                                  help='takes regular expression(s) as value to be used for package searches')),

        # flags
        (['-g', '--gmt'], dict(dest='utc', action='store_true',
                               help='sets the display time format to GMT/UTC')),
        (['-n', '--nocolor'], dict(dest='color', action='store_false', default=True,
                                   help='disables the colored output')),
        (['-q'], dict(dest='query', action='store_true',
                      help='queries the gentoo.linuxhowtos.org database '
                           'if no local emerge was found')),
        (['-S'], dict(dest='case_sensitive', action='store_true',
                      help='enables case sensitive matching')),
    ]

    def __init__(self, arguments):
        self.arguments = arguments
        self.argument_parser = argparse.ArgumentParser()
        self._configure_arguments()

        self._processor_configuration = {}
        self._parser_configuration = {}
        self._output_configuration = {}

    def _configure_arguments(self):
        """Configures arguments."""
        for args, kwargs in self.ARGUMENTS:
            self.argument_parser.add_argument(*args, **kwargs)

    def parse_arguments(self):
        """
        Parses, sanity-checks and evaluates arguments and derives configuration.

        realizes: R-CONF-CLI-006
        """
        parsed_args = self.argument_parser.parse_args(self.arguments)

        if not parsed_args.sub_commands:
            raise KeyError("At least one sub-command argument needed.")
        elif len(parsed_args.sub_commands) == 1:
            processor_name = parsed_args.sub_commands[0]
        elif set(parsed_args.sub_commands) == {self.PROCESSORS.MERGE, self.PROCESSORS.UNMERGE}:
            processor_name = self.PROCESSORS.MERGE_UNMERGE
        else:
            raise KeyError("Not more than one sub-command allowed (except 'merge' and 'unmerge').")

        if parsed_args.query and processor_name not in self.PROCESSORS.PROCESSORS_ALLOW_QUERY:
            raise KeyError("Query flag '-q' not allowed for '{}'.".format(processor_name))

        if (parsed_args.name or parsed_args.search) and processor_name not in self.PROCESSORS.PROCESSORS_ALLOW_NAME:
            raise KeyError("Package name(s) or search arguments '-s' not allowed for '{}'.".format(processor_name))

        if not (parsed_args.name or parsed_args.search) and processor_name in self.PROCESSORS.PROCESSORS_REQUIRE_NAME:
            raise KeyError("At least one package name(s) or search arguments '-s' required for '{}'."
                           .format(processor_name))

        date_count = len(parsed_args.date) if parsed_args.date else 0
        if date_count > 2:
            raise KeyError("Up to two dates ('--date') may be given. Got {}.".format(date_count))

        self._processor_configuration.update(name=processor_name, query=parsed_args.query)
        self._parser_configuration.update(file_names=parsed_args.logfile,
                                          package_names=parsed_args.name if parsed_args.name else None,
                                          search_reg_exps=parsed_args.search,
                                          case_sensitive=parsed_args.case_sensitive,
                                          dates=parsed_args.date)
        self._output_configuration.update(utc=parsed_args.utc,
                                          color=parsed_args.color)

    @property
    def parser_configuration(self):
        return self._parser_configuration

    @property
    def processor_configuration(self):
        return self._processor_configuration

    @property
    def output_configuration(self):
        return self._output_configuration
