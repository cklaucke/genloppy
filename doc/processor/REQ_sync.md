# R-PROCESSOR-SYNC-001: Provide a list sync processor implementation #
*genloppy* SHALL provide a list sync processor implementation.
The list sync processor SHALL be subclassed from base output processor.

# R-PROCESSOR-SYNC-002: Header and trailer #
The list merge and unmerge processor SHALL set
-   `HEADER` to an empty string,
-   `TRAILER` to an empty string.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-SYNC-003: Callbacks #
The list sync processor SHALL add a callback `process` for entry type `sync`.

*   related to: R-PROCESSOR-API-003

# R-PROCESSOR-SYNC-004: Process callback implementation #
On retrieving a `sync` log entry the process callback SHALL call `sync_item` of its associated output implementation with
-   `timestamp` as `timestamp`.
