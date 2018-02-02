

class Interface:
    """
    Provides the processor API

    realizes: R-PROCESSOR-API-001
    """
    def __init__(self):
        raise NotImplementedError

    @property
    def callbacks(self):
        """Returns a dict of modes and associated callbacks to be subscribed.

        realizes: R-PROCESSOR-API-003"""
        raise NotImplementedError

    def pre_process(self):
        """Does pre-processing before parsing has begun.

        realizes: R-PROCESSOR-API-002"""
        raise NotImplementedError

    def post_process(self):
        """Does post-processing after parsing has finished.

        realizes: R-PROCESSOR-API-004"""
        raise NotImplementedError


# processor names
# TODO: may also be provided by the processing class itself
CURRENT = "current"
INFO = "info"
MERGE = "merge"
MERGE_UNMERGE = "merge_unmerge"
PRETEND = "pretend"
SYNC = "sync"
TIME = "time"
UNMERGE = "unmerge"
VERSION = "version"

# processors that require at least one name and/or search regex
# TODO: may also be provided by a class property
PROCESSORS_REQUIRE_NAME = {INFO, TIME}

# processors that allow for name and/or search regex
# TODO: may also be provided by a class property
PROCESSORS_ALLOW_NAME = {MERGE, MERGE_UNMERGE, UNMERGE} | PROCESSORS_REQUIRE_NAME

# processors that allow
# TODO: may also be provided by a class property
PROCESSORS_ALLOW_QUERY = {CURRENT, PRETEND, TIME}

# processor name mapping to implementation
# TODO: may also be built through introspection?
PROCESSORS = {
    CURRENT: Interface,
    INFO: Interface,
    MERGE: Interface,
    MERGE_UNMERGE: Interface,
    PRETEND: Interface,
    SYNC: Interface,
    TIME: Interface,
    UNMERGE: Interface,
    VERSION: Interface,
}
