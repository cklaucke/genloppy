import sys
from collections import defaultdict
from functools import reduce

from genloppy.parser.entry_handler import EntryHandler
from genloppy.parser.pms import EMERGE_PRETEND_ENTRY_TYPES
from genloppy.parser.tokenizer import Tokenizer
from genloppy.processor.base import BaseOutput
from genloppy.processor.duration import Duration


class Pretend(BaseOutput):
    """Pretend processor implementation
    realizes: R-PROCESSOR-PRETEND-001
    """
    HEADER = "These are the pretended packages: (this may take a while; wait...)\n"
    TRAILER = "Estimated update time: {}."

    def __init__(self, pretend_stream=sys.stdin, **kwargs):
        """Adds callback for 'pretend'.
        realizes: R-PROCESSOR-PRETEND-002
        realizes: R-PROCESSOR-PRETEND-004
        """
        duration = Duration(self.process)
        super().__init__(callbacks=duration.callbacks, **kwargs)
        self.pretend_stream = pretend_stream
        self.durations = defaultdict(list)
        self.pretended_packages = []

    def _parse_pretended_packages(self):
        tp = Tokenizer(EMERGE_PRETEND_ENTRY_TYPES, entry_handler=EntryHandler(), echo=True)
        tp.entry_handler.register_listener(
            lambda properties: self.pretended_packages.append(properties["atom_base"]),
            "pretended_package")
        tp.tokenize(self.pretend_stream)

    def pre_process(self):
        """Does pre-processing before parsing has begun.
        realizes: R-PROCESSOR-PRETEND-003
        """
        super().pre_process()
        self._parse_pretended_packages()

    def process(self, properties, duration):
        """Stores the duration using the atom_base.
        :param properties: properties/token of the entry
        :param duration: the duration of the merge

        realizes: R-PROCESSOR-PRETEND-005"""
        self.durations[properties["atom_base"]].append(duration)

    def _calculate_durations(self, package):
        durations = self.durations[package]
        if durations:
            return [min(durations), sum(durations) / len(durations), max(durations), durations[-1]]

    def _estimate_duration(self):
        durations = None
        skipped_packages = [package for package in self.pretended_packages if not self.durations[package]]
        if len(skipped_packages) < len(self.pretended_packages):
            durations = reduce(lambda x, y: [x[i] + y[i] for i in range(4)],
                               (self._calculate_durations(package) for package in self.pretended_packages
                                if package not in skipped_packages),
                               # [min, avg, max, recent]
                               [0, 0, 0, 0])
        return skipped_packages, durations

    def _print_package_durations(self):
        max_package_name_len = max((len(x) for x in self.pretended_packages))
        self.output.package_duration_header(max_package_name_len)
        for package in self.pretended_packages:
            package_durations = self._calculate_durations(package)
            if package_durations:
                self.output.package_duration(max_package_name_len, package, package_durations)

    def post_process(self):
        """Does post-processing after parsing has finished.
        realizes: R-PROCESSOR-PRETEND-006
        """
        skipped_packages, durations = self._estimate_duration()
        self.output.message("\n")
        for package in skipped_packages:
            self.output.message(f"!!! Error: couldn't get previous merge of {package}; skipping...")
        if skipped_packages:
            self.output.message("\n")
        if durations:
            self._print_package_durations()
            self.output.message("")
            self.output.message(self.TRAILER.format(self.output.format_duration_estimation(durations)))
        else:
            self.output.message("!!! Error: estimated time unknown.")
