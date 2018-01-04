__author__ = "cklaucke"

"""
Provides log entry specific item classes

realizes: R-ITEM-001
"""


class BaseItem:
    """
    An item consisting of a timestamp only.

    realizes: R-ITEM-002
    """
    def __init__(self, timestamp):
        """
        Initialize a BaseItem.

        :param timestamp: seconds since 1970-01-01 00:00:00 UTC
        """
        self.timestamp = timestamp


class PackageItem(BaseItem):
    """
    An item which additionally holds package information.

    realizes: R-ITEM-003
    """
    def __init__(self, timestamp, name, version):
        """
        Initialize a PackageItem.

        :param timestamp: seconds since 1970-01-01 00:00:00 UTC
        :param name: atom base
        :param version: atom version
        """
        super().__init__(timestamp)
        self.name = name
        self.version = version


class MergeItem(PackageItem):
    """
    An item which additionally holds merge information.

    realizes: R-ITEM-004
    """
    def __init__(self, timestamp_begin, timestamp_end, name, version):
        """
        Initialize a MergeItem.

        :param timestamp_begin: begin of the operation in seconds since 1970-01-01 00:00:00 UTC
        :param timestamp_end: end of the operation in seconds since 1970-01-01 00:00:00 UTC
        :param name: atom base
        :param version: atom version
        """
        super().__init__(timestamp_begin, name, version)
        self.timestamp_end = timestamp_end
        self.duration = timestamp_end - timestamp_begin


class UnmergeItem(PackageItem):
    """
    An item which additionally holds unmerge information.

    realizes: R-ITEM-005
    """
    def __init__(self, timestamp, name, version):
        """
        Initialize an UnmergeItem.

        :param timestamp: end of the operation in seconds since 1970-01-01 00:00:00 UTC
        :param name: atom base
        :param version: atom version
        """
        super().__init__(timestamp, name, version)


class SyncItem(BaseItem):
    """
    An item which additionally holds a repository name.

    realizes: R-ITEM-006
    """
    def __init__(self, timestamp, repo_name):
        """
        Initialize an SyncItem.

        :param timestamp: end of the operation in seconds since 1970-01-01 00:00:00 UTC
        :param repo_name: name of the repository
        """
        super().__init__(timestamp)
        self.repo_name = repo_name
