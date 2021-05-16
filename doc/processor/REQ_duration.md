# R-PROCESSOR-DURATION-001: Provide a duration processor implementation #
*genloppy* SHALL provide a duration processor implementation.
The duration processor SHALL be subclassed from base processor.

# R-PROCESSOR-DURATION-002: Initialization #
The duration processor SHALL take
-   `callback` which takes two arguments: `properties` and `duration`.

# R-PROCESSOR-DURATION-003: Callbacks #
The duration processor SHALL add callbacks `merge_begin` and `merge_end` for entry types `merge_begin` and `merge_end` respectively.

*   related to: R-PROCESSOR-API-003

# R-PROCESSOR-DURATION-004: merge_begin callback implementation #
On retrieving a `merge_begin` log entry the merge_begin callback SHALL save the properties / tokens.

# R-PROCESSOR-DURATION-005: merge_end callback implementation #
On retrieving a `merge_end` log entry the merge_end callback SHALL:
1. Check if the saved `merge_begin` properties matches the `merge_end` properties by comparing
    -   `count_n`
    -   `count_m`,
    -   `atom`.
2. If the check succeeded calculate the duration by subtracting timestamp of `merge_begin` from timestamp of `merge_end`.
Call the `callback` with `properties` from `merge_end` and duration.

The callback SHALL reset the saved properties before returning.
