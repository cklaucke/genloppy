from unittest.mock import MagicMock, call

from genloppy.processor.base import Base
from genloppy.processor.duration import Duration
from tests.processor import MergeProperties


def test_01_base_subclass():
    """Tests that the duration processor subclassed from Base.
    tests: R-PROCESSOR-DURATION-001"""
    assert issubclass(Duration, Base)


def test_02_initialization():
    """Tests initialization and callbacks of the duration processor
    tests: R-PROCESSOR-DURATION-002
    tests: R-PROCESSOR-DURATION-003"""
    m = MagicMock()
    duration = Duration(m.callback)

    assert duration.callback == m.callback
    assert "merge_begin" in duration.callbacks
    assert "merge_end" in duration.callbacks


def test_03_merge_end_mismatch():
    """Tests that mismatching merge entries are ignored.
    tests: R-PROCESSOR-DURATION-004
    tests: R-PROCESSOR-DURATION-005"""
    m = MagicMock()
    duration = Duration(m.callback)
    merge_begin = MergeProperties(
        timestamp=0,
        atom="cat/package-3.2.1",
        atom_base="cat/package",
        atom_version="3.2.1",
        count_n="11",
        count_m="23"
    )
    merge_ends = [
        MergeProperties(
            timestamp=0,
            atom="dog/package-3.2.1",
            atom_base="dog/package",
            atom_version="3.2.1",
            count_n="11",
            count_m="23"
        ),
        MergeProperties(
            timestamp=0,
            atom="cat/package-3.2.2",
            atom_base="cat/package",
            atom_version="3.2.2",
            count_n="11",
            count_m="23"
        ),
        MergeProperties(
            timestamp=0,
            atom="cat/package-3.2.1",
            atom_base="cat/package",
            atom_version="3.2.1",
            count_n="12",
            count_m="23"
        ),
        MergeProperties(
            timestamp=0,
            atom="cat/package-3.2.1",
            atom_base="cat/package",
            atom_version="3.2.1",
            count_n="11",
            count_m="22"
        ),
    ]
    for merge_end in merge_ends:
        duration.callbacks["merge_begin"](merge_begin._asdict())
        duration.callbacks["merge_end"](merge_end._asdict())

    assert not m.method_calls


def test_04_merge_end_orphaned_merge_end():
    """Tests that a merge_end w/o a merge_begin is ignored.
    tests: R-PROCESSOR-DURATION-004
    tests: R-PROCESSOR-DURATION-005"""
    m = MagicMock()
    duration = Duration(m.callback)
    merge_end = MergeProperties(
        timestamp=0,
        atom="cat/package-3.2.1",
        atom_base="cat/package",
        atom_version="3.2.1",
        count_n="11",
        count_m="23"
    )
    duration.callbacks["merge_end"](merge_end._asdict())
    assert not m.method_calls


def test_05_duration_calculation_success():
    """Tests a duration calculation for a good case.
    tests: R-PROCESSOR-DURATION-004
    tests: R-PROCESSOR-DURATION-005"""
    m = MagicMock()
    duration = Duration(m.callback)
    merge_properties = [
        mp := MergeProperties(
            timestamp=1337,
            atom="cat/package-3.2.1",
            atom_base="cat/package",
            atom_version="3.2.1",
            count_n="11",
            count_m="23"
        ),
        mp._replace(timestamp=3677820),
    ]
    duration.callbacks["merge_begin"](merge_properties[0]._asdict())
    duration.callbacks["merge_end"](merge_properties[1]._asdict())

    assert m.method_calls == [
        call.callback(
            merge_properties[1]._asdict(),
            merge_properties[1].timestamp - merge_properties[0].timestamp
        )
    ]
