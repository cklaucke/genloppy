# R-PARSER-FILTER-REGEX-001: Provide a regex filter for entry events #
*genloppy* SHALL provide a regular expression filter for entry events.
The package filter SHALL be subclassed from entry handler wrapper.

* depends on: R-PARSER-ENTRY-HANDLER-WRAPPER-001

# R-PARSER-FILTER-REGEX-002: Initialization #
The package filter SHALL be initialized with
-   an iterable of regular expressions and
-   optionally, boolean keyword `case_sensitive` which defaults to `False`.

If a provided regular expression is not valid a `RuntimeError` SHALL be raised.

# R-PARSER-FILTER-REGEX-003: Predicate implementation #
The predicate SHALL return `True` if any of the stored regular expressions matches.

The regular expressions SHALL be matched against the value of key `atom`. If the key does not exist the predicate SHALL return `False`.

If `case_sensitive` is `False` the case of the regular expression SHALL be ignored.
Otherwise the case MUST not be ignored.

* realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-005
