import bz2
import gzip
import lzma
import re
from contextlib import closing
from pathlib import Path

from genloppy.parser.pms import LOG_ENTRY_PATTERN

RE_LOG_ENTRY = re.compile(LOG_ENTRY_PATTERN)


def _open_log_file(filename):
    return closing(_get_opener(filename)(filename, mode='rt'))


def _get_opener(filename):
    file_types = [(open, UnicodeDecodeError),
                  (gzip.open, OSError),
                  (bz2.open, OSError),
                  (lzma.open, lzma.LZMAError)]
    for opener, exception in file_types:
        try:
            with opener(filename) as f:
                f.readline()
            return opener
        except exception:
            continue
    raise RuntimeError("Unknown file format.")


def _get_log_entry_timestamp(log_entry):
    m = RE_LOG_ENTRY.match(log_entry)
    if m:
        return int(m.group('timestamp'))
    else:
        raise ValueError("Malformed log file.")


def _check_log_files(log_files):
    not_found_log_files = list(filename for filename in log_files if not Path(filename).is_file())
    malformed_log_files = list()

    def _well_formed_log_file(filename):
        try:
            with _open_log_file(filename) as f:
                _get_log_entry_timestamp(f.readline())
        except (AttributeError, RuntimeError, ValueError, IndexError):
            malformed_log_files.append(filename)

    for filename in filter(lambda f: f not in not_found_log_files, log_files):
        _well_formed_log_file(filename)

    messages = []
    if not_found_log_files:
        messages.append("The following log file(s) were not found: {}."
                        .format(", ".join(map(lambda x: "'{}'".format(x), not_found_log_files))))
    if malformed_log_files:
        messages.append("The format of the following log file(s) is unexpected: {}."
                        .format(", ".join(map(lambda x: "'{}'".format(x), malformed_log_files))))
    if messages:
        raise RuntimeError(" ".join(messages))


def _order_log_files(log_files):
    if len(log_files) == 1:
        return log_files

    log_file_timestamp = list()
    for log_file in log_files:
        with _open_log_file(log_file) as f:
            log_file_timestamp.append((log_file,
                                       _get_log_entry_timestamp(f.readline())))
    return list(map(lambda item: item[0], sorted(log_file_timestamp, key=lambda item: item[1])))


class LogFiles:
    """Handles processing of log files (multiple and compressed).
    realizes: R-LOG-FILES-001
    """

    def __init__(self, file_names):
        """Validates and orders the provided log file names.
        realizes: R-LOG-FILES-003
        realizes: R-LOG-FILES-004
        """
        _file_names = list(file_names)
        _check_log_files(_file_names)
        self.file_names = _order_log_files(_file_names)

    def __iter__(self):
        """Returns the file handles of the log files one by one in chronological order (ascending).
        :return: handle of the log file in the line
        realizes: R-LOG-FILES-004
        """
        for file_name in self.file_names:
            with _open_log_file(file_name) as f:
                yield f
