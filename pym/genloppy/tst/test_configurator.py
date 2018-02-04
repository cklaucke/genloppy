from genloppy.configurator import CommandLine
import genloppy.processor as processor

import nose.tools


def test_01_positional_arguments_accepted():
    """
    Tests that positional argument 'package names' are accepted.

    tests: R-CONF-CLI-001
    tests: R-CONF-CLI-002
    """
    CommandLine(["-l", "pkg1"]).parse_arguments()
    CommandLine(["-l", "pkg1", "cat/pkg2"]).parse_arguments()


def test_02a_sub_command_arguments_without_name_accepted():
    """
    Tests that sub-commands 'current', 'list', 'pretend',
    'rsync', 'unmerge' and 'version' without a given name or
    search expression are accepted.

    tests: R-CONF-CLI-001
    tests: R-CONF-CLI-003
    tests: R-CONF-CLI-006
    """
    sub_commands_long = ["--current", "--list", "--pretend",
                         "--rsync", "--unmerge", "--version"]
    sub_commands_short = ["-c", "-l", "-p", "-r", "-u", "-v"]

    for sub_command in sub_commands_long:
        CommandLine([sub_command]).parse_arguments()

    for sub_command in sub_commands_short:
        CommandLine([sub_command]).parse_arguments()


def test_02b_sub_command_arguments_with_optional_name_accepted():
    """
    Tests that sub-commands 'list' and 'unmerge' with a given name or
    search expression are accepted.

    tests: R-CONF-CLI-001
    tests: R-CONF-CLI-002
    tests: R-CONF-CLI-003
    tests: R-CONF-CLI-006
    """
    sub_commands_long = ["--list", "--unmerge"]
    sub_commands_short = ["-l", "-u"]

    for sub_command in sub_commands_long:
        CommandLine([sub_command, "pkg"]).parse_arguments()

    for sub_command in sub_commands_long:
        CommandLine([sub_command, "-s", "pkg"]).parse_arguments()

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "pkg"]).parse_arguments()

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "-s", "pkg"]).parse_arguments()

    CommandLine(sub_commands_long + ["pkg"]).parse_arguments()
    CommandLine(sub_commands_short + ["-s", "pkg"]).parse_arguments()


def test_02c_sub_command_arguments_with_required_name_accepted():
    """
    Tests that sub-commands 'info' and 'time' with a given name or
    search expression are accepted.

    tests: R-CONF-CLI-001
    tests: R-CONF-CLI-002
    tests: R-CONF-CLI-003
    tests: R-CONF-CLI-006
    """
    sub_commands_long = ["--info", "--time"]
    sub_commands_short = ["-i", "-t"]

    for sub_command in sub_commands_long:
        CommandLine([sub_command, "pkg"]).parse_arguments()

    for sub_command in sub_commands_long:
        CommandLine([sub_command, "-s", "pkg"]).parse_arguments()

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "pkg"]).parse_arguments()

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "-s", "pkg"]).parse_arguments()


def test_02d_sub_command_arguments_with_unexpected_name_rejected():
    """
    Tests that sub-commands 'current', 'pretend',
    'rsync', 'version' with a given name or
    search expression are rejected.

    tests: R-CONF-CLI-001
    tests: R-CONF-CLI-002
    tests: R-CONF-CLI-003
    tests: R-CONF-CLI-006
    """
    sub_commands_long = ["--current", "--pretend",
                         "--rsync", "--version"]
    sub_commands_short = ["-c", "-p", "-r", "-v"]

    for sub_command in sub_commands_long:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command, "pkg"]).parse_arguments()

    for sub_command in sub_commands_long:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command, "--search", "regex"]).parse_arguments()

    for sub_command in sub_commands_short:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command, "pkg"]).parse_arguments()

    for sub_command in sub_commands_short:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command, "-s", "regex"]).parse_arguments()


def test_02e_sub_command_arguments_with_missing_name_rejected():
    """
    Tests that sub-commands 'info' and 'time' with a given name or
    search expression are accepted.

    tests: R-CONF-CLI-001
    tests: R-CONF-CLI-002
    tests: R-CONF-CLI-003
    tests: R-CONF-CLI-006
    """
    sub_commands_long = ["--info", "--time"]
    sub_commands_short = ["-i", "-t"]

    for sub_command in sub_commands_long:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command]).parse_arguments()

    for sub_command in sub_commands_short:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command]).parse_arguments()


def test_02f_missing_sub_command_rejected():
    """
    Tests that a missing sub-command is rejected.

    tests: R-CONF-CLI-006
    """
    with nose.tools.assert_raises(KeyError):
        CommandLine([]).parse_arguments()


def test_02g_allowed_combination_of_sub_command_accepted():
    """
    Tests that an allowed combination of sub-commands is accepted.

    tests: R-CONF-CLI-006
    """
    CommandLine(["--list", "--unmerge"]).parse_arguments()
    CommandLine(["--list", "-u"]).parse_arguments()
    CommandLine(["-u", "-l"]).parse_arguments()


def test_02h_forbidden_combination_of_sub_command_rejected():
    """
    Tests that a forbidden combination of sub-commands is rejected.

    tests: R-CONF-CLI-006
    """
    with nose.tools.assert_raises(KeyError):
        CommandLine(["--list", "--time", "pkg"]).parse_arguments()
    with nose.tools.assert_raises(KeyError):
        CommandLine(["--pretend", "-u"]).parse_arguments()
    with nose.tools.assert_raises(KeyError):
        CommandLine(["-c", "-t", "pkg"]).parse_arguments()


def test_02i_sub_command_help_accepted():
    """
    Tests that sub-command 'help' is accepted.

    tests: R-CONF-CLI-003
    """
    with nose.tools.assert_raises(SystemExit) as cm:
        CommandLine(["--help"]).parse_arguments()
    assert cm.exception.code == 0

    with nose.tools.assert_raises(SystemExit):
        CommandLine(["-h"]).parse_arguments()
    assert cm.exception.code == 0


def test_03_unknown_arguments_rejected():
    """
    Tests that unknown arguments are rejected.

    tests: R-CONF-CLI-006
    """

    with nose.tools.assert_raises(SystemExit) as cm:
        CommandLine(["--magic"]).parse_arguments()
    assert cm.exception.code != 0

    with nose.tools.assert_raises(SystemExit) as cm:
        CommandLine(["-m"]).parse_arguments()
    assert cm.exception.code != 0


def test_04a_key_value_arguments_accepted():
    """
    Tests that key-value arguments 'date',
    'logfile' and 'search' are accepted.

    tests: R-CONF-CLI-004
    """
    key_value_long = ["--date", "--search"]
    key_value_short = ["-f", "-s"]

    for key_value in key_value_long:
        CommandLine(["-l", key_value, "dummy"]).parse_arguments()

    for key_value in key_value_short:
        CommandLine(["-l", key_value, "dummy"]).parse_arguments()


def test_04b_missing_value_for_key_value_arguments():
    """
    Tests that key-value arguments are rejected if a value is not given.

    tests: R-CONF-CLI-004
    tests: R-CONF-CLI-006
    """
    key_value_long = ["--date", "--search"]
    key_value_short = ["-f", "-s"]

    for key_value in key_value_long:
        with nose.tools.assert_raises(SystemExit) as cm:
            CommandLine(["-l", key_value]).parse_arguments()
        assert cm.exception.code != 0

    for key_value in key_value_short:
        with nose.tools.assert_raises(SystemExit) as cm:
            CommandLine(["-l", key_value]).parse_arguments()
        assert cm.exception.code != 0


def test_04c_multiple_key_value_arguments_accepted():
    """
    Tests that multiple key-value arguments 'date',
    'logfile' and 'search' are accepted.

    tests: R-CONF-CLI-004
    """
    key_value_long = ["--date", "--search"]
    key_value_short = ["-f", "-s"]

    for key_value in key_value_long:
        CommandLine(["-l", key_value, "dummy", key_value, "dummy"]).parse_arguments()

    for key_value in key_value_short:
        CommandLine(["-l", key_value, "dummy", key_value, "dummy"]).parse_arguments()


def test_04d_three_date_arguments_rejected():
    """
    Tests that three 'date' arguments are rejected.

    tests: R-CONF-CLI-006
    """

    with nose.tools.assert_raises(KeyError):
        CommandLine(["-l"] + 3*["--date", "5"]).parse_arguments()


def test_05a_flag_arguments_accepted():
    """
    Tests that global flag arguments 'gmt', 'nocolor'
    and 'case sensitive' are accepted.

    tests: R-CONF-CLI-005
    """
    flag_long = ["--gmt", "--nocolor"]
    flag_short = ["-g", "-n", "-S"]

    for flag in flag_long:
        CommandLine(["-l", flag]).parse_arguments()

    for flag in flag_short:
        CommandLine(["-l", flag]).parse_arguments()


def test_05b_flag_query_argument_accepted():
    """
    Tests that flag arguments 'query'
    is accepted for 'current', 'pretend' and 'time'.

    tests: R-CONF-CLI-005
    tests: R-CONF-CLI-006
    """
    sub_commands = ["-c", "-p"]

    for sub_command in sub_commands:
        CommandLine(["-q", sub_command]).parse_arguments()

    CommandLine(["-q", "-t", "pkg"]).parse_arguments()


def test_05c_flag_query_argument_rejected():
    """
    Tests that flag arguments 'query'
    is rejected for unsupported sub-commands.

    tests: R-CONF-CLI-005
    tests: R-CONF-CLI-006
    """
    sub_commands = ["-i", "-l", "-u"]
    for sub_command in sub_commands:
        with nose.tools.assert_raises(KeyError):
            CommandLine(["-q", sub_command, "pkg"]).parse_arguments()

    sub_commands = ["-r", "-v"]
    for sub_command in sub_commands:
        with nose.tools.assert_raises(KeyError):
            CommandLine(["-q", sub_command]).parse_arguments()


def test_07a_get_default_configuration():
    """
    Tests that default configuration is obtained.

    tests: R-CONF-CLI-007
    """
    c = CommandLine(["-l"])
    c.parse_arguments()
    nose.tools.assert_dict_equal(c.parser_configuration,
                                 dict(file_names=None,
                                      package_names=None,
                                      search_reg_exps=None,
                                      case_sensitive=False,
                                      dates=None))
    nose.tools.assert_dict_equal(c.processor_configuration,
                                 dict(name=processor.MERGE, query=False))
    nose.tools.assert_dict_equal(c.output_configuration,
                                 dict(gmt=False,
                                      nocolor=False))


def test_07b_get_configurations():
    """
    Tests that the correct configuration is obtained for different arguments.

    tests: R-CONF-CLI-007
    """
    conf_test = [
        (["-l", "pkg"],
         dict(file_names=None, package_names=["pkg"], search_reg_exps=None, case_sensitive=False, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=False, nocolor=False)),
        (["-l", "pkg", "pkg2"],
         dict(file_names=None, package_names=["pkg", "pkg2"], search_reg_exps=None, case_sensitive=False, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=False, nocolor=False)),
        (["-l", "-f", "file1", "-f", "file2"],
         dict(file_names=["file1", "file2"], package_names=None, search_reg_exps=None, case_sensitive=False, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=False, nocolor=False)),
        (["-l", "--date", "1", "--date", "1337"],
         dict(file_names=None, package_names=None, search_reg_exps=None, case_sensitive=False, dates=["1", "1337"]),
         dict(name=processor.MERGE, query=False),
         dict(gmt=False, nocolor=False)),
        (["-l", "--search", ".*", "-s", "foo[a-z]+"],
         dict(file_names=None, package_names=None, search_reg_exps=[".*", "foo[a-z]+"], case_sensitive=False, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=False, nocolor=False)),
        (["-l", "-g"],
         dict(file_names=None, package_names=None, search_reg_exps=None, case_sensitive=False, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=True, nocolor=False)),
        (["-l", "-n"],
         dict(file_names=None, package_names=None, search_reg_exps=None, case_sensitive=False, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=False, nocolor=True)),
        (["-l", "--gmt", "--nocolor"],
         dict(file_names=None, package_names=None, search_reg_exps=None, case_sensitive=False, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=True, nocolor=True)),
        (["-t", "-q", "cat/pkg"],
         dict(file_names=None, package_names=["cat/pkg"], search_reg_exps=None, case_sensitive=False, dates=None),
         dict(name=processor.TIME, query=True),
         dict(gmt=False, nocolor=False)),
        (["-l", "-S"],
         dict(file_names=None, package_names=None, search_reg_exps=None, case_sensitive=True, dates=None),
         dict(name=processor.MERGE, query=False),
         dict(gmt=False, nocolor=False)),
    ]

    for args, expected_parser_configuration, expected_processor_configuration, \
            expected_output_configuration in conf_test:
                c = CommandLine(args)
                c.parse_arguments()
                nose.tools.assert_dict_equal(c.parser_configuration, expected_parser_configuration)
                nose.tools.assert_dict_equal(c.processor_configuration, expected_processor_configuration)
                nose.tools.assert_dict_equal(c.output_configuration, expected_output_configuration)
