# R-PROCESSOR-SYNC-001: Provide a list sync processor implementation #
*genloppy* SHALL provide a list sync processor implementation.
The list sync processor SHALL be subclassed from base output processor.

# R-PROCESSOR-SYNC-002: Pre-processing implementation #
The list sync processor SHALL call `message` of its associated output implementation with an empty string.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-SYNC-003: Callbacks #
The list sync processor SHALL add a callback `process` for `sync` log entries.

*   related to: R-PROCESSOR-API-003

# R-PROCESSOR-SYNC-004: Post-processing implementation #
The list sync processor SHALL call `message` of its associated output implementation with an empty string.

*   related to: R-PROCESSOR-API-004

# R-PROCESSOR-SYNC-005: Process callback implementation #
On retrieving a `sync` log entry the process callback SHALL call `sync_item` of its associated output implementation with
-   `timestamp` as `timestamp`.
