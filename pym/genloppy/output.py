from datetime import datetime, timezone


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


class Output(Interface):
    """Provides the output implementation
    realizes: R-OUTPUT-001
    realizes: R-OUTPUT-002"""
    DATE_FORMAT = "{0:%c}"
    MERGE_FORMAT = 5 * " " + "{} >>> {}-{}"
    UNMERGE_FORMAT = 5 * " " + "{} <<< {}-{}"

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

    def _format_date(self, timestamp):
        """Formats dates.
        realizes: R-OUTPUT-005"""
        return self.DATE_FORMAT.format(datetime.fromtimestamp(int(timestamp), tz=self.tz))

    def message(self, message):
        """"Prints a message
        realizes: R-OUTPUT-006"""
        print(message)

    def merge_item(self, timestamp, name, version):
        """"Prints a merge item
        realizes: R-OUTPUT-007"""
        print(self.MERGE_FORMAT.format(self._format_date(timestamp), name, version))

    def unmerge_item(self, timestamp, name, version):
        """"Prints a unmerge item
        realizes: R-OUTPUT-008"""
        print(self.UNMERGE_FORMAT.format(self._format_date(timestamp), name, version))
