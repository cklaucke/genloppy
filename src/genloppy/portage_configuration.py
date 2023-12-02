"""
Portage configuration accessor implementation
realizes: R-PORTAGE-CONFIG-001
"""
import os.path
import subprocess
from typing import Final

PORTAGEQ: Final = "portageq"
ENV_EMERGE_LOG_DIR: Final = "EMERGE_LOG_DIR"
ENV_EPREFIX: Final = "EPREFIX"
DEFAULT_LOG_DIR: Final = os.path.join("var", "log")
DEFAULT_LOG_FILENAME: Final = "emerge.log"


class PortageConfigurationError(Exception):
    ...


def _get_portage_env_var(environment_variable: str) -> str:
    """
    Queries 'portageq' for the given environment variable.

    :param environment_variable: name of the environment variable
    :return: the value of the environment variable; if environment variable is not set an
                PortageConfigurationError will be raised
    """
    env_var = environment_variable
    cp = subprocess.run([PORTAGEQ, "envvar", env_var], stdout=subprocess.PIPE, text=True)
    if cp.returncode == 0:
        return cp.stdout.strip()

    raise PortageConfigurationError(f"Cannot query environment variable '{env_var}'.")


def get_default_emerge_log_file() -> str:
    """
    Gets the system's default emerge log file by querying portage.

    :return: path to the system's default log file

    realizes: R-PORTAGE-CONFIG-002
    """
    try:
        emerge_log_dir = _get_portage_env_var(ENV_EMERGE_LOG_DIR)
    except PortageConfigurationError:
        e_prefix = _get_portage_env_var(ENV_EPREFIX).lstrip(os.sep)
        emerge_log_dir = os.path.join(os.sep, e_prefix, DEFAULT_LOG_DIR)

    return os.path.join(emerge_log_dir, DEFAULT_LOG_FILENAME)
