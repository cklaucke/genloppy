from genloppy.configurator import CommandLine
import genloppy.processor as processor

import nose.tools


def test_01_positional_arguments_accepted():
    """
    Tests that positional argument 'package names' are accepted.

    tests: R-CONF-CLI-001
    tests: R-CONF-CLI-002
    """
    CommandLine(["-l", "pkg1"])
    CommandLine(["-l", "pkg1", "cat/pkg2"])


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
        CommandLine([sub_command])

    for sub_command in sub_commands_short:
        CommandLine([sub_command])


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
        CommandLine([sub_command, "pkg"])

    for sub_command in sub_commands_long:
        CommandLine([sub_command, "-s", "pkg"])

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "pkg"])

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "-s", "pkg"])

    CommandLine(sub_commands_long + ["pkg"])
    CommandLine(sub_commands_short + ["-s", "pkg"])


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
        CommandLine([sub_command, "pkg"])

    for sub_command in sub_commands_long:
        CommandLine([sub_command, "-s", "pkg"])

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "pkg"])

    for sub_command in sub_commands_short:
        CommandLine([sub_command, "-s", "pkg"])


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
            CommandLine([sub_command, "pkg"])

    for sub_command in sub_commands_long:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command, "--search", "regex"])

    for sub_command in sub_commands_short:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command, "pkg"])

    for sub_command in sub_commands_short:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command, "-s", "regex"])


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
            CommandLine([sub_command])

    for sub_command in sub_commands_short:
        with nose.tools.assert_raises(KeyError):
            CommandLine([sub_command])


def test_02f_missing_sub_command_rejected():
    """
    Tests that a missing sub-command is rejected.

    tests: R-CONF-CLI-006
    """
    with nose.tools.assert_raises(KeyError):
        CommandLine([])


def test_02g_allowed_combination_of_sub_command_accepted():
    """
    Tests that an allowed combination of sub-commands is accepted.

    tests: R-CONF-CLI-006
    """
    CommandLine(["--list", "--unmerge"])
    CommandLine(["--list", "-u"])
    CommandLine(["-u", "-l"])


def test_02h_forbidden_combination_of_sub_command_rejected():
    """
    Tests that a forbidden combination of sub-commands is rejected.

    tests: R-CONF-CLI-006
    """
    with nose.tools.assert_raises(KeyError):
        CommandLine(["--list", "--time", "pkg"])
    with nose.tools.assert_raises(KeyError):
        CommandLine(["--pretend", "-u"])
    with nose.tools.assert_raises(KeyError):
        CommandLine(["-c", "-t", "pkg"])


def test_02i_sub_command_help_accepted():
    """
    Tests that sub-command 'help' is accepted.

    tests: R-CONF-CLI-003
    """
    with nose.tools.assert_raises(SystemExit) as cm:
        CommandLine(["--help"])
    assert cm.exception.code == 0

    with nose.tools.assert_raises(SystemExit):
        CommandLine(["-h"])
    assert cm.exception.code == 0


def test_03_unknown_arguments_rejected():
    """
    Tests that unknown arguments are rejected.

    tests: R-CONF-CLI-006
    """

    with nose.tools.assert_raises(SystemExit) as cm:
        CommandLine(["--magic"])
    assert cm.exception.code != 0

    with nose.tools.assert_raises(SystemExit) as cm:
        CommandLine(["-m"])
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
        CommandLine(["-l", key_value, "dummy"])

    for key_value in key_value_short:
        CommandLine(["-l", key_value, "dummy"])


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
            CommandLine(["-l", key_value])
        assert cm.exception.code != 0

    for key_value in key_value_short:
        with nose.tools.assert_raises(SystemExit) as cm:
            CommandLine(["-l", key_value])
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
        CommandLine(["-l", key_value, "dummy", key_value, "dummy"])

    for key_value in key_value_short:
        CommandLine(["-l", key_value, "dummy", key_value, "dummy"])


def test_04d_three_date_arguments_rejected():
    """
    Tests that three 'date' arguments are rejected.

    tests: R-CONF-CLI-006
    """

    with nose.tools.assert_raises(KeyError):
        CommandLine(["-l"] + 3*["--date", "5"])


def test_05a_flag_arguments_accepted():
    """
    Tests that global flag arguments 'gmt', 'nocolor'
    and 'case sensitive' are accepted.

    tests: R-CONF-CLI-005
    """
    flag_long = ["--gmt", "--nocolor"]
    flag_short = ["-g", "-n", "-S"]

    for flag in flag_long:
        CommandLine(["-l", flag])

    for flag in flag_short:
        CommandLine(["-l", flag])


def test_05b_flag_query_argument_accepted():
    """
    Tests that flag arguments 'query'
    is accepted for 'current', 'pretend' and 'time'.

    tests: R-CONF-CLI-005
    tests: R-CONF-CLI-006
    """
    sub_commands = ["-c", "-p"]

    for sub_command in sub_commands:
        CommandLine(["-q", sub_command])

    CommandLine(["-q", "-t", "pkg"])


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
            CommandLine(["-q", sub_command, "pkg"])

    sub_commands = ["-r", "-v"]
    for sub_command in sub_commands:
        with nose.tools.assert_raises(KeyError):
            CommandLine(["-q", sub_command])


def test_07a_get_default_configuration():
    """
    Tests that default configuration is obtained.

    tests: R-CONF-CLI-007
    """
    c = CommandLine(["-l"])
    assert c.names is None
    assert c.processor_name == processor.MERGE
    assert c.file_names is None
    assert c.dates is None
    assert c.search_reg_exp is None
    assert c.gmt is False
    assert c.nocolor is False
    assert c.query is False
    assert c.case_sensitive is False


def test_07b_get_configurations():
    """
    Tests that the correct configuration is obtained for different arguments.

    tests: R-CONF-CLI-007
    """
    conf_test = [
        (["-l", "pkg"],
         (["pkg"], processor.MERGE, None, None, None, False, False, False, False)),
        (["-l", "pkg", "pkg2"],
         (["pkg", "pkg2"], processor.MERGE, None, None, None, False, False, False, False)),
        (["-l", "-f", "file1", "-f", "file2"],
         (None, processor.MERGE, ["file1", "file2"], None, None, False, False, False, False)),
        (["-l", "--date", "1", "--date", "1337"],
         (None, processor.MERGE, None, ["1", "1337"], None, False, False, False, False)),
        (["-l", "--search", ".*", "-s", "foo[a-z]+"],
         (None, processor.MERGE, None, None, [".*", "foo[a-z]+"], False, False, False, False)),
        (["-l", "-g"],
         (None, processor.MERGE, None, None, None, True, False, False, False)),
        (["-l", "-n"],
         (None, processor.MERGE, None, None, None, False, True, False, False)),
        (["-l", "--gmt", "--nocolor"],
         (None, processor.MERGE, None, None, None, True, True, False, False)),
        (["-t", "-q", "cat/pkg"],
         (["cat/pkg"], processor.TIME, None, None, None, False, False, True, False)),
        (["-l", "-S"],
         (None, processor.MERGE, None, None, None, False, False, False, True)),
    ]

    for args, expectation in conf_test:
        c = CommandLine(args)
        nose.tools.assert_equal((c.names, c.processor_name, c.file_names, c.dates, c.search_reg_exp,
                                 c.gmt, c.nocolor, c.query, c.case_sensitive), expectation)
