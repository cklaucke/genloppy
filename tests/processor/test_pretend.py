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
    assert "merge_begin" in pretend.callbacks
    assert "merge_end" in pretend.callbacks
    assert pretend.callbacks["merge_begin"] is not None
    assert pretend.callbacks["merge_end"] is not None


def test_04_post_processing():
    """Tests that pretend processor calls message with the expected post-processing text.
    tests: R-PROCESSOR-PRETEND-002
    tests: R-PROCESSOR-PRETEND-006"""
    m = MagicMock()
    pretend = Pretend(output=m)
    pretend.post_process()
    assert m.method_calls == [call.message("\n"),
                              call.message("!!! Error: estimated time unknown.")]


def test_05_pretend_processing_simple():
    """Tests a simple pretend output w/ well known package.
    tests: R-PROCESSOR-PRETEND-003
    tests: R-PROCESSOR-PRETEND-005
    tests: R-PROCESSOR-PRETEND-006"""
    m = MagicMock()
    m.format_duration_estimation.return_value = "mocked duration estimation"
    duration = 3677820

    pretend = Pretend(output=m, pretend_stream=StringIO("[ebuild   N    ] cat/package-4.0.3"))
    pretend.pre_process()
    merge_properties = dict(timestamp=3679157, atom="cat/package-3.2.1", atom_base="cat/package", atom_version="3.2.1",
                            count_n="11",
                            count_m="23")
    pretend.process(merge_properties, duration)
    pretend.post_process()

    max_package_name_len = len(merge_properties["atom_base"])
    assert m.method_calls == [call.message("These are the pretended packages: (this may take a while; wait...)\n"),
                              call.message("\n"),
                              call.package_duration_header(max_package_name_len),
                              call.package_duration(max_package_name_len, merge_properties["atom_base"],
                                                    4 * [duration]),
                              call.message(''),
                              call.format_duration_estimation([duration, duration, duration, duration]),
                              call.message("Estimated update time: mocked duration estimation.")]


def test_08_pretend_processing_one_unknown():
    """Tests a simple pretend output w/ an unknown package
    tests: R-PROCESSOR-PRETEND-003
    tests: R-PROCESSOR-PRETEND-005
    tests: R-PROCESSOR-PRETEND-006"""
    m = MagicMock()
    m.format_duration_estimation.return_value = "mocked duration estimation"
    duration = 3677820

    pretend = Pretend(output=m, pretend_stream=StringIO("[ebuild   N    ] cat/package-4.0.3\n"
                                                        "[ebuild   N    ] dog/package-4.0.3\n"))
    pretend.pre_process()
    merge_properties = dict(timestamp=3679157, atom="cat/package-3.2.1", atom_base="cat/package", atom_version="3.2.1",
                            count_n="11",
                            count_m="23")
    pretend.process(merge_properties, duration)
    pretend.post_process()

    max_package_name_len = len(merge_properties["atom_base"])
    assert m.method_calls == [call.message("These are the pretended packages: (this may take a while; wait...)\n"),
                              call.message("\n"),
                              call.message("!!! Error: couldn't get previous merge of dog/package; skipping..."),
                              call.message("\n"),
                              call.package_duration_header(max_package_name_len),
                              call.package_duration(max_package_name_len, merge_properties["atom_base"],
                                                    4 * [duration]),
                              call.message(''),
                              call.format_duration_estimation([duration, duration, duration, duration]),
                              call.message("Estimated update time: mocked duration estimation.")]


def test_09_pretend_processing_all_unknown():
    """Tests a simple pretend output w/o a known package
    tests: R-PROCESSOR-PRETEND-003
    tests: R-PROCESSOR-PRETEND-005
    tests: R-PROCESSOR-PRETEND-006"""
    m = MagicMock()
    pretend = Pretend(output=m, pretend_stream=StringIO("[ebuild   N    ] cat/package-4.0.3"))
    pretend.pre_process()
    pretend.post_process()
    assert m.method_calls == [call.message("These are the pretended packages: (this may take a while; wait...)\n"),
                              call.message("\n"),
                              call.message("!!! Error: couldn't get previous merge of cat/package; skipping..."),
                              call.message("\n"),
                              call.message("!!! Error: estimated time unknown.")]
