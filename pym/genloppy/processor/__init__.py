from genloppy.processor.api import Interface
from genloppy.processor.merge import Merge
from genloppy.processor.unmerge import Unmerge
from genloppy.processor.merge_unmerge import MergeUnmerge

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
    MERGE: Merge,
    MERGE_UNMERGE: MergeUnmerge,
    PRETEND: Interface,
    SYNC: Interface,
    TIME: Interface,
    UNMERGE: Unmerge,
    VERSION: Interface,
}


class ProcessorFactory:
    """
    Provides the factory to instantiate the processors.

    realizes: R-PROCESSOR-001
    """
    def __init__(self):
        pass

    def create(self, processor_name, **kwargs):
        return PROCESSORS[processor_name](**kwargs)
