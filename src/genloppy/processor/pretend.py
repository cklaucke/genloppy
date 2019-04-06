import functools
import sys
from collections import defaultdict

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
        super().__init__(**kwargs)
        duration = Duration(self.process)
        self._add_callbacks(**duration.callbacks)
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

    def _estimate_duration(self):
        average = 0
        skipped_packages = []
        for package in self.pretended_packages:
            durations = self.durations[package]
            if durations:
                average += functools.reduce(lambda x, y: x + y, map(lambda t: t / len(durations), durations))
            else:
                skipped_packages.append(package)
        return average, skipped_packages

    def post_process(self):
        """Does post-processing after parsing has finished.
        realizes: R-PROCESSOR-PRETEND-006
        """
        estimated_duration, skipped_packages = self._estimate_duration()
        self.output.message("\n")
        for package in skipped_packages:
            self.output.message("!!! Error: couldn't get previous merge of {}; skipping...".format(package))
        if skipped_packages:
            self.output.message("\n")
        if estimated_duration:
            self.output.message(
                self.TRAILER.format(self.output.format_duration(estimated_duration, show_seconds=False)))
        else:
            self.output.message("!!! Error: estimated time unknown.")
