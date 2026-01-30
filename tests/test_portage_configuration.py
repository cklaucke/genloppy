import os.path
from subprocess import CompletedProcess
from unittest.mock import patch

import pytest

from genloppy.portage_configuration import PortageConfigurationError, get_default_emerge_log_file


def test_01_get_default_emerge_log_file_with_emerge_log_dir():
    """Tests that a default log file comprised of the provided emerge log dir is returned.
    tests: R-PORTAGE-CONFIG-001
    tests: R-PORTAGE-CONFIG-002
    """
    emerge_log_dir = "/foo"

    def run_side_effects(*args, **_kwargs):
        assert args[0][0] == "portageq"
        assert args[0][1] == "envvar"
        if args[0][2] == "EMERGE_LOG_DIR":
            return CompletedProcess("", 0, stdout=emerge_log_dir)
        return None

    with patch("subprocess.run") as subprocess_run_mock:
        subprocess_run_mock.side_effect = run_side_effects

        assert get_default_emerge_log_file() == os.path.join(emerge_log_dir, "emerge.log")


def test_02_get_default_emerge_log_file_without_emerge_log_dir():
    """Tests that a default log file comprised of the provided eprefix, "var" and "log" is returned.
    tests: R-PORTAGE-CONFIG-001
    tests: R-PORTAGE-CONFIG-002
    """
    e_prefix = "prefix"

    def run_side_effects(*args, **_kwargs):
        assert args[0][0] == "portageq"
        assert args[0][1] == "envvar"
        if args[0][2] == "EMERGE_LOG_DIR":
            return CompletedProcess("", 1, stdout=None)
        if args[0][2] == "EPREFIX":
            return CompletedProcess("", 0, stdout=e_prefix)
        return None

    with patch("subprocess.run") as subprocess_run_mock:
        subprocess_run_mock.side_effect = run_side_effects

        assert get_default_emerge_log_file() == os.path.join(os.sep, e_prefix, "var", "log", "emerge.log")


def test_03_get_default_emerge_log_file_without_eprefix_fails():
    """Tests that an exception is raised if neither emerge log dir nor eprefix can be determined.
    tests: R-PORTAGE-CONFIG-001
    tests: R-PORTAGE-CONFIG-002
    """

    def run_side_effects(*args, **_kwargs):
        first_arg = args[0]
        assert first_arg[0] == "portageq"
        assert first_arg[1] == "envvar"
        if first_arg[2] == "EMERGE_LOG_DIR" or first_arg[2] == "EPREFIX":
            return CompletedProcess("", 1, stdout=None)
        return None

    with patch("subprocess.run") as subprocess_run_mock:
        subprocess_run_mock.side_effect = run_side_effects

        with pytest.raises(PortageConfigurationError) as exception:
            get_default_emerge_log_file()

        assert exception.value.args[0] == "Cannot query environment variable 'EPREFIX'."


def test_04_get_default_emerge_log_file_without_portageq_fails():
    """Tests that an exception is raised if neither emerge log dir nor eprefix can be determined.
    tests: R-PORTAGE-CONFIG-001
    tests: R-PORTAGE-CONFIG-002
    """

    def run_side_effects(*_args, **_kwargs):
        return CompletedProcess("", 127)

    with patch("subprocess.run") as subprocess_run_mock:
        subprocess_run_mock.side_effect = run_side_effects

        with pytest.raises(PortageConfigurationError) as exception:
            get_default_emerge_log_file()

        assert exception.value.args[0].startswith("Cannot query environment variable")
