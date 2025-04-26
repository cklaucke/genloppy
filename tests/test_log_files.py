from os.path import dirname, join

import pytest

from genloppy.log_files import LogFiles

TEST_DATA_DIR = "test_log_files"


def test_01a_unknown_file_format_raises():
    """Tests that an error is raised if the given log file is of unknown format
    tests: R-LOG-FILES-001
    tests: R-LOG-FILES-003"""
    log_files = [join(dirname(__file__), TEST_DATA_DIR, "garbage")]
    with pytest.raises(RuntimeError) as exception:
        LogFiles(log_files)

    assert exception.value.args[0] == f"The format of the following log file(s) is unexpected: '{log_files[0]}'."


def test01b_malformed_log_files_raises():
    """Tests that an error is raised if given log files are malformed
    tests: R-LOG-FILES-001
    tests: R-LOG-FILES-003"""
    log_files = [
        join(dirname(__file__), TEST_DATA_DIR, file)
        for file in ["malformed.log", "malformed.log.gz", "malformed.log.bz2", "malformed.log.lzma"]
    ]

    with pytest.raises(RuntimeError) as exception:
        LogFiles(log_files)

    assert exception.value.args[0].startswith("The format of the following log file(s) is unexpected: ")
    assert exception.value.args[0].index(log_files[0])
    assert exception.value.args[0].index(log_files[1])
    assert exception.value.args[0].index(log_files[2])
    assert exception.value.args[0].index(log_files[3])


def test_01c_non_existent_log_file_raises():
    """Tests that an error is raised if the given log file does not exist
    tests: R-LOG-FILES-001
    tests: R-LOG-FILES-003"""
    log_files = [join(dirname(__file__), TEST_DATA_DIR, "non_existing.log")]
    with pytest.raises(RuntimeError) as exception:
        LogFiles(log_files)

    assert exception.value.args[0] == f"The following log file(s) were not found: '{log_files[0]}'."


def test_02a_order_single_log_file_succeeds():
    """Tests that ordering a single file succeeds, i.e. does nothing
    tests: R-LOG-FILES-001
    tests: R-LOG-FILES-004"""
    log_files = [join(dirname(__file__), TEST_DATA_DIR, "good.1.log")]
    lf = LogFiles(log_files)

    assert lf.file_names == log_files


def test_02b_order_multiple_log_file_succeeds():
    """Tests that multiple file are ordered chronologically (ascending)
    tests: R-LOG-FILES-001
    tests: R-LOG-FILES-004"""
    log_files_ordered = [
        join(dirname(__file__), TEST_DATA_DIR, "good.1.log"),
        join(dirname(__file__), TEST_DATA_DIR, "good.2.log"),
    ]
    log_files_unordered = [
        join(dirname(__file__), TEST_DATA_DIR, "good.2.log"),
        join(dirname(__file__), TEST_DATA_DIR, "good.1.log"),
    ]

    lf = LogFiles(log_files_ordered)
    fd = list(lf)
    assert len(fd) == 2
    assert lf.file_names == log_files_ordered
    lf = LogFiles(log_files_unordered)
    assert lf.file_names == log_files_ordered

    log_files_ordered_compressed = [x + ".gz" for x in log_files_ordered]
    lf = LogFiles(log_files_ordered_compressed)
    assert lf.file_names == log_files_ordered_compressed
    lf = LogFiles(x + ".gz" for x in log_files_unordered)
    assert lf.file_names == log_files_ordered_compressed

    log_files_ordered_compressed = [x + ".bz2" for x in log_files_ordered]
    lf = LogFiles(log_files_ordered_compressed)
    assert lf.file_names == log_files_ordered_compressed
    lf = LogFiles(x + ".bz2" for x in log_files_unordered)
    assert lf.file_names == log_files_ordered_compressed

    log_files_ordered_compressed = [x + ".lzma" for x in log_files_ordered]
    lf = LogFiles(log_files_ordered_compressed)
    assert lf.file_names == log_files_ordered_compressed
    lf = LogFiles(x + ".lzma" for x in log_files_unordered)
    assert lf.file_names == log_files_ordered_compressed
