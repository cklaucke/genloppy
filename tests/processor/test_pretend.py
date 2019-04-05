from io import StringIO
from unittest.mock import MagicMock
from unittest.mock import call

from genloppy.processor.base import BaseOutput
from genloppy.processor.pretend import Pretend


def test_01_base_output_subclass():
    """Tests that pretend processor is BaseOutput subclass.
    tests: R-PROCESSOR-PRETEND-001"""
    assert issubclass(Pretend, BaseOutput)


def test_02_pre_processing():
    """Tests that pretend processor calls message with the expected pre-processing text.
    tests: R-PROCESSOR-PRETEND-002
    tests: R-PROCESSOR-PRETEND-003"""
    m = MagicMock()
    pretend = Pretend(output=m, pretend_stream=StringIO())
    pretend.pre_process()
    assert m.method_calls == [call.message("These are the pretended packages: (this may take a while; wait...)\n")]


def test_03_callback_added():
    """Tests that pretend processor added callbacks.
    tests: R-PROCESSOR-PRETEND-004"""
    pretend = Pretend(output=None)
    assert pretend.callbacks == dict(merge_begin=pretend.merge_begin,
                                     merge_end=pretend.merge_end)


def test_04_post_processing():
    """Tests that pretend processor calls message with the expected post-processing text.
    tests: R-PROCESSOR-PRETEND-002
    tests: R-PROCESSOR-PRETEND-007"""
    m = MagicMock()
    pretend = Pretend(output=m)
    pretend.post_process()
    assert m.method_calls == [call.message("\n"),
                              call.message("!!! Error: estimated time unknown.")]


def test_05_merge_end_mismatch():
    """Tests that mismatching merge entries produce a warning.
    tests: R-PROCESSOR-PRETEND-006"""
    m = MagicMock()
    pretend = Pretend(output=m)
    merge_begin = dict(timestamp=0, atom_base="cat/package", atom_version="3.2.1", count_n="11", count_m="23")
    merge_ends = [dict(timestamp=0, atom_base="dog/package", atom_version="3.2.1", count_n="11", count_m="23"),
                  dict(timestamp=0, atom_base="cat/package", atom_version="3.2.2", count_n="11", count_m="23"),
                  dict(timestamp=0, atom_base="cat/package", atom_version="3.2.1", count_n="12", count_m="23"),
                  dict(timestamp=0, atom_base="cat/package", atom_version="3.2.1", count_n="11", count_m="22"),
                  dict(timestamp=3677820, atom_base="cat/package", atom_version="3.2.1", count_n="11", count_m="23")]
    for merge_end in merge_ends:
        pretend.merge_begin(merge_begin)
        pretend.merge_end(merge_end)
    assert m.method_calls == [call.message("[WARN] Non-matching begin and end merge found. Skipping."),
                              call.message("[WARN] Non-matching begin and end merge found. Skipping."),
                              call.message("[WARN] Non-matching begin and end merge found. Skipping."),
                              call.message("[WARN] Non-matching begin and end merge found. Skipping.")]


def test_06_merge_end_orphaned_merge_end():
    """Tests that a merge_end w/o a merge_begin produces a warning.
    test: R-PROCESSOR-PRETEND-006"""
    m = MagicMock()
    pretend = Pretend(output=m)
    merge_end = dict(timestamp=0, atom_base="cat/package", atom_version="3.2.1", count_n="11", count_m="23")
    pretend.merge_end(merge_end)
    assert m.method_calls == [call.message("[WARN] End merge without begin merge found. Skipping.")]


def test_07_pretend_processing_simple():
    """Tests a simple pretend output w/ well known package.
    tests: R-PROCESSOR-PRETEND-003
    tests: R-PROCESSOR-PRETEND-005
    tests: R-PROCESSOR-PRETEND-006
    tests: R-PROCESSOR-PRETEND-007"""
    m = MagicMock()
    pretend = Pretend(output=m, pretend_stream=StringIO("[ebuild   N    ] cat/package-4.0.3"))
    pretend.pre_process()
    merge_properties = [dict(timestamp=0, atom_base="cat/package", atom_version="3.2.1", count_n="11", count_m="23"),
                        dict(timestamp=3677820, atom_base="cat/package", atom_version="3.2.1", count_n="11",
                             count_m="23")]
    pretend.merge_begin(merge_properties[0])
    pretend.merge_end(merge_properties[1])
    pretend.post_process()
    assert m.method_calls == [call.message("These are the pretended packages: (this may take a while; wait...)\n"),
                              call.message("\n"),
                              call.message("Estimated update time: 42 days, 13 hours, 37 minutes.")]


def test_08_pretend_processing_one_unkown():
    """Tests a simple pretend output w/ an unknown package
    tests: R-PROCESSOR-PRETEND-003
    tests: R-PROCESSOR-PRETEND-005
    tests: R-PROCESSOR-PRETEND-006
    tests: R-PROCESSOR-PRETEND-007"""
    m = MagicMock()
    pretend = Pretend(output=m, pretend_stream=StringIO("[ebuild   N    ] cat/package-4.0.3\n"
                                                        "[ebuild   N    ] dog/package-4.0.3\n"))
    pretend.pre_process()
    merge_properties = [dict(timestamp=0, atom_base="cat/package", atom_version="3.2.1", count_n="11", count_m="23"),
                        dict(timestamp=3677820, atom_base="cat/package", atom_version="3.2.1", count_n="11",
                             count_m="23")]
    pretend.merge_begin(merge_properties[0])
    pretend.merge_end(merge_properties[1])
    pretend.post_process()
    assert m.method_calls == [call.message("These are the pretended packages: (this may take a while; wait...)\n"),
                              call.message("\n"),
                              call.message("!!! Error: couldn't get previous merge of dog/package; skipping..."),
                              call.message("\n"),
                              call.message("Estimated update time: 42 days, 13 hours, 37 minutes.")]


def test_09_pretend_processing_all_unkown():
    """Tests a simple pretend output w/o a known package
    tests: R-PROCESSOR-PRETEND-003
    tests: R-PROCESSOR-PRETEND-005
    tests: R-PROCESSOR-PRETEND-006
    tests: R-PROCESSOR-PRETEND-007"""
    m = MagicMock()
    pretend = Pretend(output=m, pretend_stream=StringIO("[ebuild   N    ] cat/package-4.0.3"))
    pretend.pre_process()
    pretend.post_process()
    assert m.method_calls == [call.message("These are the pretended packages: (this may take a while; wait...)\n"),
                              call.message("\n"),
                              call.message("!!! Error: couldn't get previous merge of cat/package; skipping..."),
                              call.message("\n"),
                              call.message("!!! Error: estimated time unknown.")]
