# R-PROCESSOR-TIME-001: Provide a time processor implementation #
*genloppy* SHALL provide a time processor implementation.
The time processor SHALL be subclassed from base output processor.

*   related to: R-PROCESSOR-BASE-OUTPUT-001

# R-PROCESSOR-TIME-002: Initialization #
The time processor SHALL operate in two modes:
-   package mode and,
-   search mode.

To determine the mode the keyword argument `active_filter` SHALL be evaluated as follows.
If `active_filter` contains `search_reg_exps` search mode SHALL be used. Otherwise package mode SHALL be used.

# R-PROCESSOR-TIME-003: Pre-process implementation #
In search mode the time processor SHALL call `message` of its associated output implementation with ` * matches found:` followed by an empty line.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-TIME-004: Callbacks #
The time processor SHALL use and instance of the duration processor initialized with
-   package mode: callback `process_package`
-   search mode: callback `process_search`.

It SHALL retrieve the callbacks of the duration processor and add them to its own callbacks.

*   related to: R-PROCESSOR-API-003
*   depends on: R-PROCESSOR-DURATION-001

# R-PROCESSOR-TIME-005: process_package callback implementation #
The callback SHALL store `timestamp`, `atom_version` and `duration` for `atom_base`.

# R-PROCESSOR-TIME-006: process_search callback implementation #
The callback SHALL call `merge_time_item` of its associated output implementation with
-   `timestamp` as `timestamp`,
-   `atom_base` as `name`,
-   `atom_version` as `version`,
-   duration.

# R-PROCESSOR-TIME-007: Post-process implementation #
The time processor SHALL *overwrite* the default implementation.

For package mode it SHALL print the stored durations lexically sorted by key `atom_base` and then in the order of appearance. First the `atom_base` SHALL be printed (` * {atom_base}`) and then all merge time item by calling `merge_time_item` of its associated output implementation with
-   `timestamp` as `timestamp`,
-   `atom_base` as `name`,
-   `atom_version` as `version`,
-   duration.

*   related to: R-PROCESSOR-API-004
