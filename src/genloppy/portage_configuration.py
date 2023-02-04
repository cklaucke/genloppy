"""
Portage configuration accessor implementation
realizes: R-PORTAGE-CONFIG-001
"""
import os.path
import subprocess

PORTAGEQ = "portageq"
ENV_EMERGE_LOG_DIR = "EMERGE_LOG_DIR"
ENV_EPREFIX = "EPREFIX"
DEFAULT_LOG_DIR = os.path.join("var", "log")
DEFAULT_LOG_FILENAME = "emerge.log"


class PortageConfigurationError(Exception):
    pass


def _get_portage_env_var(environment_variable, default=None):
    """
    Queries 'portageq' for the given environment variable.

    :param environment_variable: name of the environment variable
    :param default: value to return if environment variable is not set
                    -- if set to None an PortageConfigurationError will be risen
    :return: the value of the environment variable
    """
    env_var = str(environment_variable)
    cp = subprocess.run([PORTAGEQ, "envvar", env_var], stdout=subprocess.PIPE, text=True)
    if cp.returncode == 0:
        return cp.stdout.strip()
    elif cp.returncode == 1 and default is not None:
        return default
    else:
        raise PortageConfigurationError(f"Cannot query environment variable '{env_var}'.")


def get_default_emerge_log_file():
    """
    Gets the system's default emerge log file by querying portage.

    :return: path to the system's default log file

    realizes: R-PORTAGE-CONFIG-002
    """
    emerge_log_dir = _get_portage_env_var(ENV_EMERGE_LOG_DIR, "")
    if not emerge_log_dir:
        e_prefix = _get_portage_env_var(ENV_EPREFIX).lstrip(os.sep)
        emerge_log_dir = os.path.join(os.sep, e_prefix, DEFAULT_LOG_DIR)

    return os.path.join(emerge_log_dir, DEFAULT_LOG_FILENAME)
