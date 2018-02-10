# R-PROCESSOR-MERGE-001: Provide a list merge processor implementation #
*genloppy* SHALL provide a list merge processor implementation.
The list merge processor SHALL be subclassed from base output processor.

# R-PROCESSOR-MERGE-002: Pre-processing implementation #
The list merge processor SHALL call `message` of its associated output implementation with ` * packages merged:` followed by an empty line.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-MERGE-003: Callbacks #
The list merge processor SHALL add a callback `process` for `merge` log entries.

*   related to: R-PROCESSOR-API-003

# R-PROCESSOR-MERGE-004: Post-processing implementation #
The list merge processor SHALL call `message` of its associated output implementation with an empty string.

*   related to: R-PROCESSOR-API-004

# R-PROCESSOR-MERGE-005: Process callback implementation #
On retrieving a `merge` log entry the process callback SHALL call `merge_item` of its associated output implementation with
-   `timestamp_end` as `timestamp`,
-   `name` as `name`,
-   `version` as `version`.
