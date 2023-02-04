from collections import defaultdict
from enum import Enum

from genloppy.processor.base import BaseOutput
from genloppy.processor.duration import Duration


class Time(BaseOutput):
    """Time processor implementation
    realizes: R-PROCESSOR-TIME-001
    """

    MODES = Enum("Mode", "package search")

    def __init__(self, active_filter=None, **kwargs):
        """Initializes the time processor.
        realizes: R-PROCESSOR-TIME-002
        realizes: R-PROCESSOR-TIME-004
        """
        if active_filter and "search_reg_exps" in active_filter:
            self.mode = self.MODES.search
            d = Duration(self.process_search)
        else:
            self.mode = self.MODES.package
            d = Duration(self.process_package)
        super().__init__(callbacks=d.callbacks, **kwargs)
        self.durations = defaultdict(list)

    def pre_process(self):
        """Does pre-processing before parsing has begun.
        realizes: R-PROCESSOR-TIME-003
        """
        if self.mode is self.MODES.search:
            self.output.message(" * matches found:\n")

    def process_package(self, properties, duration):
        """Stores properties and duration in package mode
        realizes: R-PROCESSOR-TIME-005
        """
        self.durations[properties["atom_base"]].append((properties, duration))

    def process_search(self, properties, duration):
        """Prints merge time items directly in search mode
        realizes: R-PROCESSOR-TIME-006
        """
        self.output.merge_time_item(properties["timestamp"], properties["atom_base"], properties["atom_version"], duration)

    def post_process(self):
        """Does post-processing after parsing has finished.
        realizes: R-PROCESSOR-TIME-007
        """
        if self.mode is self.MODES.package:
            atom_bases_merges = ((atom_base, self.durations[atom_base]) for atom_base in sorted(self.durations))
            for atom_base, merges in atom_bases_merges:
                self.output.message(f" * {atom_base}:\n")
                for merge in merges:
                    self.output.merge_time_item(merge[0]["timestamp"], merge[0]["atom_base"], merge[0]["atom_version"], merge[1])
