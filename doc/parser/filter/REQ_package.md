# R-PARSER-FILTER-PACKAGE-001: Provide a package filter for entry events #
*genloppy* SHALL provide a package filter for entry events.
The package filter SHALL be subclassed from entry handler wrapper.

* depends on: R-PARSER-ENTRY-HANDLER-WRAPPER-001

# R-PARSER-FILTER-PACKAGE-002: Initialization #
The package filter SHALL be initialized with
-   an iterable of packages and
-   optionally, boolean keyword `case_sensitive` which defaults to `False`.

If a provided package does not conform to qualified package name (`atom_base`) or package name (`package_name`) a `RuntimeError` SHALL be raised.

* depends on: R-PARSER-PMS-002

# R-PARSER-FILTER-PACKAGE-003: Predicate implementation #
The predicate SHALL return `True` if any of the stored packages matches.

Package matching:
-   qualified package name: if it is equal to the given value of key `atom_base`,
-   package name: if it is equal to the given value of key `package_name`.

If `case_sensitive` is `False` the case of the stored package name and the given value SHALL be ignored.
Otherwise the case MUST not be ignored.

If the required keys do not exist the predicate SHALL return `False`.

* realizes: R-PARSER-ENTRY-HANDLER-WRAPPER-005
