# R-PROCESSOR-UNMERGE-001: Provide a list unmerge processor implementation #
*genloppy* SHALL provide a list unmerge processor implementation.
The list unmerge processor SHALL be subclassed from base output processor.

# R-PROCESSOR-UNMERGE-002: Pre-processing implementation #
The list unmerge processor SHALL call `message` of its associated output implementation with ` * packages unmerged:` followed by an empty line.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-UNMERGE-003: Callbacks #
The list unmerge processor SHALL add a callback `process` for `unmerge` log entries.

*   related to: R-PROCESSOR-API-003

# R-PROCESSOR-UNMERGE-004: Post-processing implementation #
The list unmerge processor SHALL call `message` of its associated output implementation with an empty string.

*   related to: R-PROCESSOR-API-004

# R-PROCESSOR-UNMERGE-005: Process callback implementation #
On retrieving a `unmerge` log entry the process callback SHALL call `unmerge_item` of its associated output implementation with
-   `timestamp` as `timestamp`,
-   `name` as `name`,
-   `version` as `version`.
