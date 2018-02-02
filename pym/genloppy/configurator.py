"""
Provides configurators
"""

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
        (['-g', '--gmt'], dict(action='store_true',
                               help='sets the display time format to GMT/UTC')),
        (['-n', '--nocolor'], dict(action='store_true',
                                   help='disables the colored output')),
        (['-q'], dict(dest='query', action='store_true',
                      help='queries the gentoo.linuxhowtos.org database '
                           'if no local emerge was found')),
        (['-S'], dict(dest='case_sensitive', action='store_true',
                      help='enables case sensitive matching')),
    ]

    def __init__(self, arguments):
        self.argument_parser = argparse.ArgumentParser()
        self.configure_arguments()

        self._processor_name = None

        self.parsed_arguments = self.argument_parser.parse_args(arguments)
        self.determine_configuration()

    def configure_arguments(self):
        """Configures arguments."""
        for args, kwargs in self.ARGUMENTS:
            self.argument_parser.add_argument(*args, **kwargs)

    def determine_configuration(self):
        """
        Sanity-checks and evaluates parsed arguments and derives configuration.

        realizes: R-CONF-CLI-006
        """
        args = self.parsed_arguments

        if not args.sub_commands:
            raise KeyError("At least one sub-command argument needed.")
        elif len(args.sub_commands) == 1:
            processor_name = args.sub_commands[0]
        elif set(args.sub_commands) == {self.PROCESSORS.MERGE, self.PROCESSORS.UNMERGE}:
            processor_name = self.PROCESSORS.MERGE_UNMERGE
        else:
            raise KeyError("Not more than one sub-command allowed (except 'merge' and 'unmerge').")

        if args.query and processor_name not in self.PROCESSORS.PROCESSORS_ALLOW_QUERY:
            raise KeyError("Query flag '-q' not allowed for '{}'.".format(processor_name))

        if (args.name or args.search) and processor_name not in self.PROCESSORS.PROCESSORS_ALLOW_NAME:
            raise KeyError("Package name(s) or search arguments '-s' not allowed for '{}'.".format(processor_name))

        if not (args.name or args.search) and processor_name in self.PROCESSORS.PROCESSORS_REQUIRE_NAME:
            raise KeyError("At least one package name(s) or search arguments '-s' required for '{}'."
                           .format(processor_name))

        date_count = len(args.date) if args.date else 0
        if date_count > 2:
            raise KeyError("Up to two dates ('--date') may be given. Got {}.".format(date_count))

        self._processor_name = processor_name

    @property
    def names(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.name if self.parsed_arguments.name else None

    @property
    def processor_name(self):
        """realizes: R-CONF-CLI-007"""
        return self._processor_name

    @property
    def file_names(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.logfile

    @property
    def dates(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.date

    @property
    def search_reg_exp(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.search

    @property
    def gmt(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.gmt

    @property
    def nocolor(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.nocolor

    @property
    def query(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.query

    @property
    def case_sensitive(self):
        """realizes: R-CONF-CLI-007"""
        return self.parsed_arguments.case_sensitive
