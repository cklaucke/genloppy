from unittest.mock import MagicMock
from unittest.mock import call

from genloppy.processor.base import BaseOutput
from genloppy.processor.time import Time


def test_01_base_output_subclass():
    """Tests that pretend processor is BaseOutput subclass.
    tests: R-PROCESSOR-PRETEND-001"""
    assert issubclass(Time, BaseOutput)


def test_02_initialization():
    """Tests initialization of the time processor.
    tests: R-PROCESSOR-TIME-002"""
    time = Time(output=None)

    assert time.mode is time.MODES.package

    time = Time(output=None, active_filter={"search_reg_exps", })

    assert time.mode is time.MODES.search


def test_03_pre_processing():
    """Tests that merge processor calls message with the expected pre-processing text.
    tests: R-PROCESSOR-TIME-003"""
    m = MagicMock()
    time = Time(output=m, active_filter={"search_reg_exps", })
    time.pre_process()

    assert m.method_calls == [call.message(" * matches found:\n")]

    m.reset_mock()
    time = Time(output=m)
    time.pre_process()

    assert not m.method_calls


def test_04_callbacks():
    """Tests that time processor added callbacks.
    tests: R-PROCESSOR-TIME-004"""
    time = Time(output=None)
    assert "merge_begin" in time.callbacks
    assert "merge_end" in time.callbacks
    assert time.callbacks["merge_begin"] is not None
    assert time.callbacks["merge_end"] is not None

    time = Time(output=None, active_filter={"search_reg_exps", })
    assert "merge_begin" in time.callbacks
    assert "merge_end" in time.callbacks
    assert time.callbacks["merge_begin"] is not None
    assert time.callbacks["merge_end"] is not None


def test_05_search_mode():
    """Tests that in search mode merge time items are printed directly.
    tests: R-PROCESSOR-TIME-006
    tests: R-PROCESSOR-TIME-007"""
    m = MagicMock()
    time = Time(output=m, active_filter={"search_reg_exps", })
    merge_properties = dict(timestamp=3679157, atom="cat/package-3.2.1", atom_base="cat/package", atom_version="3.2.1",
                            count_n="11",
                            count_m="23")
    time.process_search(merge_properties, 3677820)
    time.post_process()

    assert m.method_calls == [call.merge_time_item(merge_properties["timestamp"], merge_properties["atom_base"],
                                                   merge_properties["atom_version"], 3677820)]


def test_06_package_mode():
    """Tests that in package mode merge time items are collected and printed afterwards.
    tests: R-PROCESSOR-TIME-005
    tests: R-PROCESSOR-TIME-007"""
    m = MagicMock()
    time = Time(output=m)
    merge_properties = [
        dict(timestamp=1, atom="cat/package-3.2.1", atom_base="cat/package", atom_version="3.2.1", count_n="11",
             count_m="23"),
        dict(timestamp=2, atom="abc/package-0.47.11", atom_base="abc/package", atom_version="0.47.11", count_n="7",
             count_m="9"),
        dict(timestamp=3, atom="cat/package-3.1.1", atom_base="cat/package", atom_version="3.1.1", count_n="1",
             count_m="1")]

    for merge_property in merge_properties:
        time.process_package(merge_property, 50)
    time.post_process()

    assert m.method_calls == [call.message(" * {}:\n".format(merge_properties[1]["atom_base"])),
                              call.merge_time_item(merge_properties[1]["timestamp"], merge_properties[1]["atom_base"],
                                                   merge_properties[1]["atom_version"], 50),
                              call.message(" * {}:\n".format(merge_properties[0]["atom_base"])),
                              call.merge_time_item(merge_properties[0]["timestamp"], merge_properties[0]["atom_base"],
                                                   merge_properties[0]["atom_version"], 50),
                              call.merge_time_item(merge_properties[2]["timestamp"], merge_properties[2]["atom_base"],
                                                   merge_properties[2]["atom_version"], 50),
                              ]
