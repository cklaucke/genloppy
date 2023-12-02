from __future__ import annotations

import bz2
import gzip
import lzma
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Iterator, TextIO

from genloppy.parser.pms import LOG_ENTRY_PATTERN

RE_LOG_ENTRY = re.compile(LOG_ENTRY_PATTERN)


@dataclass
class Opener:
    callback: Callable[..., TextIO]
    exception: type[Exception]


OPENER = [
    Opener(open, UnicodeDecodeError),
    Opener(gzip.open, OSError),
    Opener(bz2.open, OSError),
    Opener(lzma.open, lzma.LZMAError),
]


def _get_opener(filename) -> Callable:
    for opener in OPENER:
        try:
            with opener.callback(filename) as f:
                f.readline()
            return opener.callback
        except opener.exception:
            continue
    raise RuntimeError("Unknown file format.")


def _open_log_file(filename: str) -> TextIO:
    return _get_opener(filename)(filename, mode="rt")


def _get_log_entry_timestamp(log_entry: str) -> int:
    m = RE_LOG_ENTRY.match(log_entry)
    if m:
        return int(m.group("timestamp"))
    else:
        raise ValueError("Malformed log file.")


def _check_log_files(log_files: Iterable[str]):
    not_found_log_files = [filename for filename in log_files if not Path(filename).is_file()]
    malformed_log_files: list[str] = []

    def _well_formed_log_file(filename: str):
        try:
            with _open_log_file(filename) as f:
                _get_log_entry_timestamp(f.readline())
        except (AttributeError, RuntimeError, ValueError, IndexError):
            malformed_log_files.append(filename)

    for filename in filter(lambda f: f not in not_found_log_files, log_files):
        _well_formed_log_file(filename)

    messages = []
    if not_found_log_files:
        _not_found_log_files_as_str = ", ".join(f"'{x}'" for x in not_found_log_files)
        messages.append(f"The following log file(s) were not found: {_not_found_log_files_as_str}.")
    if malformed_log_files:
        _malformed_log_files_as_str = ", ".join(f"'{x}'" for x in malformed_log_files)
        messages.append(f"The format of the following log file(s) is unexpected: {_malformed_log_files_as_str}.")
    if messages:
        raise RuntimeError(" ".join(messages))


@dataclass
class _LogFileTimeStamp:
    filename: str
    timestamp: int

    def __lt__(self, other: _LogFileTimeStamp) -> bool:
        return self.timestamp < other.timestamp


def _order_log_files(log_files: list[str]) -> list[str]:
    if len(log_files) == 1:
        return log_files

    log_file_timestamps: list[_LogFileTimeStamp] = []
    for log_file in log_files:
        with _open_log_file(log_file) as f:
            timestamp = _get_log_entry_timestamp(f.readline())
            log_file_timestamps.append(_LogFileTimeStamp(log_file, timestamp))

    return [log_file.filename for log_file in sorted(log_file_timestamps)]


class LogFiles:
    """Handles processing of log files (multiple and compressed).
    realizes: R-LOG-FILES-001
    """

    def __init__(self, file_names: Iterable[str]) -> None:
        """Validates and orders the provided log file names.
        realizes: R-LOG-FILES-003
        realizes: R-LOG-FILES-004
        """
        _file_names = list(file_names)
        _check_log_files(_file_names)
        self.file_names = _order_log_files(_file_names)

    def __iter__(self) -> Iterator[TextIO]:
        """Returns the file handles of the log files one by one in chronological order (ascending).
        :return: handle of the log file in the line
        realizes: R-LOG-FILES-004
        """
        for file_name in self.file_names:
            with _open_log_file(file_name) as f:
                yield f
