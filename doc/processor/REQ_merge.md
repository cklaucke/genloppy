# R-PROCESSOR-MERGE-001: Provide a list merge processor implementation #
*genloppy* SHALL provide a list merge processor implementation.
The list merge processor SHALL be subclassed from base output processor.

# R-PROCESSOR-MERGE-002: Header and trailer #
The list merge processor SHALL set
-   `HEADER` to ` * packages merged:` followed by an empty line,
-   `TRAILER` to an empty string.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-MERGE-003: Callbacks #
The list merge processor SHALL add a callback `process` for entry type `merge_end`.

*   related to: R-PROCESSOR-API-003

# R-PROCESSOR-MERGE-004: Process callback implementation #
On retrieving a `merge_end` log entry the process callback SHALL call `merge_item` of its associated output implementation with
-   `timestamp` as `timestamp`,
-   `atom_base` as `name`,
-   `atom_version` as `version`.
