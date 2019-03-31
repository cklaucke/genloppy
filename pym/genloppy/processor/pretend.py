import functools
import sys
from collections import defaultdict

from genloppy.parser.entry_handler import EntryHandler
from genloppy.parser.pms import EMERGE_PRETEND_ENTRY_TYPES
from genloppy.parser.tokenizer import Tokenizer
from genloppy.processor.base import BaseOutput


class Pretend(BaseOutput):
    """Pretend processor implementation
    realizes: R-PROCESSOR-PRETEND-001
    """
    HEADER = "These are the pretended packages: (this may take a while; wait...)\n"
    TRAILER = "Estimated update time: {}."

    DAY_FORMAT = defaultdict(lambda: "{days} days")
    DAY_FORMAT[0] = ""
    DAY_FORMAT[1] = "{days} day"

    HOUR_FORMAT = defaultdict(lambda: "{hours} hours")
    HOUR_FORMAT[0] = ""
    HOUR_FORMAT[1] = "{hours} hour"

    MINUTE_FORMAT = defaultdict(lambda: "{minutes} minutes")
    MINUTE_FORMAT[0] = ""
    MINUTE_FORMAT[1] = "{minutes} minute"

    def __init__(self, pretend_stream=sys.stdin, **kwargs):
        """Adds callback for 'pretend'.
        realizes: R-PROCESSOR-PRETEND-002
        realizes: R-PROCESSOR-PRETEND-004
        """
        super().__init__(**kwargs)
        self._add_callbacks(merge_begin=self.merge_begin,
                            merge_end=self.merge_end)
        self.pretend_stream = pretend_stream
        self.current_merge = None
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

    def merge_begin(self, properties):
        """Saves the properties of the merge_begin entry
        realizes: R-PROCESSOR-PRETEND-005
        """
        self.current_merge = properties

    def merge_end(self, properties):
        """Determines the merge duration of a matching merge_end entry
        realizes: R-PROCESSOR-PRETEND-006
        """
        if self.current_merge:
            keys = ["atom_base", "atom_version", "count_m", "count_n"]
            if all(self.current_merge[key] == properties[key] for key in keys):
                duration = int(properties["timestamp"]) - int(self.current_merge["timestamp"])
                self.durations[properties["atom_base"]].append(duration)
            else:
                self.output.message("[WARN] Non-matching begin and end merge found. Skipping.")
        else:
            self.output.message("[WARN] End merge without begin merge found. Skipping.")
        self.current_merge = None

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

    def _duration_human_readable(self, duration):
        days, remainder = divmod(int(duration), 60 * 60 * 24)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes = remainder // 60
        duration_parts = [self.DAY_FORMAT[days].format(days=days),
                          self.HOUR_FORMAT[hours].format(hours=hours),
                          self.MINUTE_FORMAT[minutes].format(minutes=minutes)]
        effective_parts = (x for x in duration_parts if x)
        return ", ".join(effective_parts)

    def post_process(self):
        """Does post-processing after parsing has finished.
        realizes: R-PROCESSOR-PRETEND-007
        """
        estimated_duration, skipped_packages = self._estimate_duration()
        self.output.message("\n")
        for package in skipped_packages:
            self.output.message("!!! Error: couldn't get previous merge of {}; skipping...".format(package))
        if skipped_packages:
            self.output.message("\n")
        if estimated_duration:
            self.output.message(self.TRAILER.format(self._duration_human_readable(estimated_duration)))
        else:
            self.output.message("!!! Error: estimated time unknown.")
