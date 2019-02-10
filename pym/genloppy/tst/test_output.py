from datetime import timezone
import locale
from os import environ
from time import tzset

from genloppy.output import Interface, Output

import pytest
from unittest.mock import patch

# since output of dates is locale-aware, only C/POSIX is tested here
locale.setlocale(locale.LC_ALL, "C")
# same with timezone
environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
tzset()


def test_01_provided_api():
    """Tests if an output API is provided.
    tests: R-OUTPUT-API-001
    tests: R-OUTPUT-API-002
    tests: R-OUTPUT-API-003
    tests: R-OUTPUT-API-004
    tests: R-OUTPUT-API-005
    tests: R-OUTPUT-API-006"""

    assert hasattr(Interface, "configure")
    assert hasattr(Interface, "message")
    assert hasattr(Interface, "merge_item")
    assert hasattr(Interface, "unmerge_item")
    assert hasattr(Interface, "sync_item")

    i = Interface()

    with pytest.raises(NotImplementedError):
        i.configure()

    # methods w/ one argument
    for method in [i.message, i.sync_item]:
        with pytest.raises(NotImplementedError):
            method(None)

    # methods w/ three arguments
    for method in [i.merge_item, i.unmerge_item]:
        with pytest.raises(NotImplementedError):
            method(None, None, None)


def test_02a_configurable_output():
    """Tests configuration of output.
    tests: R-OUTPUT-001
    tests: R-OUTPUT-003
    tests: R-OUTPUT-004
    """
    out = Output()
    assert out.color == True
    assert out.tz == None
    out.configure(color=False)
    assert out.color == False
    out.configure(utc=True)
    assert out.tz == timezone.utc


def test_02b_output_date_formatting():
    """Tests that dates are formatted according to the current locale (here POSIX).
    tests: R-OUTPUT-005"""
    out = Output()
    assert out._format_date(0) == "Wed Dec 31 19:00:00 1969"
    out.configure(utc=True)
    assert out._format_date(0) == "Thu Jan  1 00:00:00 1970"
    assert out._format_date("1342421337") == "Mon Jul 16 06:48:57 2012"
    out.configure(utc=False)
    assert out._format_date("1342421337") == "Mon Jul 16 02:48:57 2012"


def test_03_output_message():
    """Tests that a message is outputted.
    tests: R-OUTPUT-002
    tests: R-OUTPUT-006"""
    out = Output()
    msg = "A message."
    with patch('builtins.print') as mock:
        out.message(msg)

    mock.assert_called_with(msg)


def test_04_output_merge_item():
    """Tests that a merge item is outputted.
    tests: R-OUTPUT-002
    tests: R-OUTPUT-007"""
    with patch.object(Output, '_format_date', return_value="") as mock_format_date:
        out = Output()
        ts = 0
        name = "cat/package"
        version = "1.33.7"
        with patch('builtins.print') as mock:
            out.merge_item(ts, name, version)

    mock_format_date.assert_called_once_with(ts)
    mock.assert_called_with(5 * " " + " >>> " + name + "-" + version)


def test_05_output_unmerge_item():
    """Tests that a unmerge item is outputted.
    tests: R-OUTPUT-002
    tests: R-OUTPUT-008"""
    with patch.object(Output, '_format_date', return_value="") as mock_format_date:
        out = Output()
        ts = 0
        name = "cat/package"
        version = "1.33.7"
        with patch('builtins.print') as mock:
            out.unmerge_item(ts, name, version)

    mock_format_date.assert_called_once_with(ts)
    mock.assert_called_with(5 * " " + " <<< " + name + "-" + version)


def test_06_output_sync_item():
    """Tests that a sync item is outputted.
    tests: R-OUTPUT-002
    tests: R-OUTPUT-009"""
    with patch.object(Output, '_format_date', return_value="") as mock_format_date:
        out = Output()
        ts = 0
        with patch('builtins.print') as mock:
            out.sync_item(ts)

    mock_format_date.assert_called_once_with(ts)
    mock.assert_called_with(5 * " " + "rsync'ed at >>> ")
