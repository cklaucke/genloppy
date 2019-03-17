# R-PROCESSOR-UNMERGE-001: Provide a list unmerge processor implementation #
*genloppy* SHALL provide a list unmerge processor implementation.
The list unmerge processor SHALL be subclassed from base output processor.

# R-PROCESSOR-UNMERGE-002: Header and trailer #
The list unmerge processor SHALL set
-   `HEADER` to ` * packages unmerged:` followed by an empty line,
-   `TRAILER` to an empty string.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-UNMERGE-003: Callbacks #
The list unmerge processor SHALL add a callback `process` for entry type `unmerge`.

*   related to: R-PROCESSOR-API-003

# R-PROCESSOR-UNMERGE-004: Process callback implementation #
On retrieving a `unmerge` log entry the process callback SHALL call `unmerge_item` of its associated output implementation with
-   `timestamp` as `timestamp`,
-   `atom_base` as `name`,
-   `atom_version` as `version`.
