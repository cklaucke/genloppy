from collections import defaultdict
from datetime import datetime
from datetime import timezone


class Interface:
    """Provides the output API
    realizes: R-OUTPUT-API-001"""

    def configure(self, **kwargs):
        """Configures the output.
        realizes: R-OUTPUT-API-002"""
        raise NotImplementedError

    def message(self, message):
        """Outputs a message
        realizes: R-OUTPUT-API-003"""
        raise NotImplementedError

    def merge_item(self, timestamp, name, version):
        """Outputs a merge item
        realizes: R-OUTPUT-API-004"""
        raise NotImplementedError

    def unmerge_item(self, timestamp, name, version):
        """Outputs a unmerge item
        realizes: R-OUTPUT-API-005"""
        raise NotImplementedError

    def sync_item(self, timestamp):
        """Outputs a sync item
        realizes: R-OUTPUT-API-006"""
        raise NotImplementedError

    def merge_time_item(self, timestamp, name, version, duration):
        """Outputs a merge time item
        realizes: R-OUTPUT-API-007"""
        raise NotImplementedError


class Output(Interface):
    """Provides the output implementation
    realizes: R-OUTPUT-001
    realizes: R-OUTPUT-002"""

    DATE_FORMAT = "{0:%c}"
    MERGE_FORMAT = 5 * " " + "{} >>> {}-{}"
    UNMERGE_FORMAT = 5 * " " + "{} <<< {}-{}"
    SYNC_FORMAT = 5 * " " + "rsync'ed at >>> {}"
    MERGE_TIME_FORMAT = MERGE_FORMAT + "\n" + 7 * " " + "merge time: {}.\n"

    DAY_FORMAT = defaultdict(lambda: "{days} days")
    DAY_FORMAT[0] = ""
    DAY_FORMAT[1] = "{days} day"

    HOUR_FORMAT = defaultdict(lambda: "{hours} hours")
    HOUR_FORMAT[0] = ""
    HOUR_FORMAT[1] = "{hours} hour"

    MINUTE_FORMAT = defaultdict(lambda: "{minutes} minutes")
    MINUTE_FORMAT[0] = ""
    MINUTE_FORMAT[1] = "{minutes} minute"

    SECOND_FORMAT = defaultdict(lambda: "{seconds} seconds")
    SECOND_FORMAT[0] = ""
    SECOND_FORMAT[1] = "{seconds} second"

    BRIEF_DURATION_FORMAT = "{hours:>3}:{minutes:02}:{seconds:02}"
    PKG_NAME_HEADING = "package"
    PKG_DURATION_SEP = " / "
    PKG_DURATION_HEADER = "{:{max_package_name_len}} " + PKG_DURATION_SEP.join(4 * ["{:>9}"])
    PKG_DURATION = "{package_name:{max_package_name_len}} {fmt_durations}"

    def __init__(self):
        self.color = True
        self.tz = None

    def configure(self, **kwargs):
        """Configures the appearance of the output.
        realizes: R-OUTPUT-004"""
        color = kwargs.get("color")
        if color is not None:
            self.color = color
        utc = kwargs.get("utc")
        if utc is not None:
            self.tz = timezone.utc if utc else None

    def format_date(self, timestamp):
        """Formats dates.
        realizes: R-OUTPUT-005"""
        return self.DATE_FORMAT.format(datetime.fromtimestamp(int(timestamp), tz=self.tz))

    def format_duration(self, duration, condensed=False):
        """Formats durations.
        realizes: R-OUTPUT-010
        :param duration: a duration in seconds
        :param condensed: if set to True omits seconds for durations >= 60 seconds
        :return: human-readable formatted duration"""
        _duration = int(duration)
        output_seconds = not condensed or (True if _duration < 60 else False)
        days, remainder = divmod(_duration, 60 * 60 * 24)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        duration_parts = [
            self.DAY_FORMAT[days].format(days=days),
            self.HOUR_FORMAT[hours].format(hours=hours),
            self.MINUTE_FORMAT[minutes].format(minutes=minutes),
            self.SECOND_FORMAT[seconds].format(seconds=seconds) if output_seconds else "",
        ]
        effective_parts = [x for x in duration_parts if x]
        if len(effective_parts) == 0:
            effective_parts = [self.SECOND_FORMAT[2].format(seconds=0)]
        if len(effective_parts) > 2:
            effective_parts = [", ".join(effective_parts[:-1]), effective_parts[-1]]
        return " and ".join(effective_parts)

    def format_brief_duration(self, duration):
        hours, remainder = divmod(int(duration), 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        return self.BRIEF_DURATION_FORMAT.format(hours=hours, minutes=minutes, seconds=seconds)

    def message(self, message):
        """Prints a message
        realizes: R-OUTPUT-006"""
        print(message)

    def merge_item(self, timestamp, name, version):
        """Prints a merge item
        realizes: R-OUTPUT-007"""
        print(self.MERGE_FORMAT.format(self.format_date(timestamp), name, version))

    def unmerge_item(self, timestamp, name, version):
        """Prints a unmerge item
        realizes: R-OUTPUT-008"""
        print(self.UNMERGE_FORMAT.format(self.format_date(timestamp), name, version))

    def sync_item(self, timestamp):
        """Prints a sync item
        realizes: R-OUTPUT-009"""
        print(self.SYNC_FORMAT.format(self.format_date(timestamp)))

    def merge_time_item(self, timestamp, name, version, duration):
        """Prints a merge time item
        realizes: R-OUTPUT-011"""
        print(self.MERGE_TIME_FORMAT.format(self.format_date(timestamp), name, version, self.format_duration(duration)))

    def _max_package_length(self, max_package_name_len):
        return max(len(self.PKG_NAME_HEADING), max_package_name_len, 1)

    def package_duration_header(self, max_package_name_len):
        print(
            self.PKG_DURATION_HEADER.format(
                self.PKG_NAME_HEADING, "min", "avg", "max", "recently", max_package_name_len=self._max_package_length(max_package_name_len)
            )
        )

    def package_duration(self, max_package_name_len, package_name, package_durations):
        fmt_durations = (self.format_brief_duration(x) for x in package_durations)
        print(
            self.PKG_DURATION.format(
                max_package_name_len=self._max_package_length(max_package_name_len),
                package_name=package_name,
                fmt_durations=self.PKG_DURATION_SEP.join(fmt_durations),
            )
        )

    def format_duration_estimation(self, durations):
        min_duration, avg_duration, max_duration, recent_duration = durations
        fmt_avg_duration = self.format_duration(avg_duration, condensed=True)
        fmt_avg_rel_min = self.format_duration(avg_duration - min_duration, condensed=True)
        fmt_avg_rel_max = self.format_duration(max_duration - avg_duration, condensed=True)
        fmt_recent_duration = self.format_duration(recent_duration, condensed=True)
        return f"{fmt_avg_duration} (-{fmt_avg_rel_min}/+{fmt_avg_rel_max}), recently: {fmt_recent_duration}"
