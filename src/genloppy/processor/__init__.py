from genloppy.processor.api import Interface
from genloppy.processor.merge import Merge
from genloppy.processor.merge_unmerge import MergeUnmerge
from genloppy.processor.pretend import Pretend
from genloppy.processor.sync import Sync
from genloppy.processor.time import Time
from genloppy.processor.unmerge import Unmerge

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
    PRETEND: Pretend,
    SYNC: Sync,
    TIME: Time,
    UNMERGE: Unmerge,
    VERSION: Interface,
}


def create(processor_name, **kwargs):
    """Returns a processor instance using processor_name.

    :param processor_name: name of the desired processor
    :param kwargs: optional keyword arguments to pass to the processor
    :returns a processor instance

    realizes: R-PROCESSOR-001"""
    return PROCESSORS[processor_name](**kwargs)
