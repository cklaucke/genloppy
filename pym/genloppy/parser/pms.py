"""
realizes: R-PARSER-PMS-001
"""
import re

# for specification see https://dev.gentoo.org/~ulm/pms/head/pms.html
CATEGORY_PATTERN = r"[A-Za-z0-9_][A-Za-z0-9+_.-]*"
PACKAGE_NAME_PATTERN = r"[A-Za-z0-9_][A-Za-z0-9+_-]*"
# according to spec "-[0-9]" starts a version (see. PMS section 3.2)
ATOM_PATTERN = r"(?P<atom_base>" + CATEGORY_PATTERN + r"/" \
               + PACKAGE_NAME_PATTERN + r")(?=-[0-9])-(?P<atom_version>[^\s]+)"

TIMESTAMP_PATTERN = r"(?P<timestamp>[0-9]+)"
COUNT_PATTERN = r"\((?P<count_n>[0-9]+) of (?P<count_m>[0-9]+)\)"

# patterns
# realizes: R-PARSER-PMS-002
MERGE_BEGIN_PATTERN = r"^" + TIMESTAMP_PATTERN + r": {2}>>> emerge " + COUNT_PATTERN + \
                      r" " + ATOM_PATTERN + r" to .*$"

# realizes: R-PARSER-PMS-003
MERGE_END_PATTERN = r"^" + TIMESTAMP_PATTERN + r": {2}::: completed emerge " + \
                    COUNT_PATTERN + r" " + ATOM_PATTERN + r" to .*$"

PRETEND_PATTERN = r"^\[e[^]]+\] " + ATOM_PATTERN

# realizes: R-PARSER-PMS-004
SYNC_COMPLETED_PATTERN = r"^" + TIMESTAMP_PATTERN + \
                         r": === Sync completed for (?P<repo_name>.*)$"

# realizes: R-PARSER-PMS-005
UNMERGE_PATTERN = r"^" + TIMESTAMP_PATTERN + r": {2}>>> unmerge success: " + ATOM_PATTERN + r"$"

# realizes: R-PARSER-PMS-006
EMERGE_LOG_ENTRY_TYPES = {
    "merge_begin": re.compile(MERGE_BEGIN_PATTERN),
    "merge_end": re.compile(MERGE_END_PATTERN),
    "unmerge": re.compile(UNMERGE_PATTERN),
    "sync": re.compile(SYNC_COMPLETED_PATTERN),
}

EMERGE_PRETEND_ENTRY_TYPES = {
    "pretended_package": re.compile(PRETEND_PATTERN)
}
