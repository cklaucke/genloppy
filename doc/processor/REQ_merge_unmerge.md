# R-PROCESSOR-MERGE-UNMERGE-001: Provide a list merge and unmerge processor implementation #
*genloppy* SHALL provide a list merge and unmerge processor implementation.
The list merge and unmerge processor SHALL be subclassed from base output processor.
It SHALL reuse the list merge and list unmerge processor implementations.

# R-PROCESSOR-MERGE-UNMERGE-002: Header and trailer #
The list merge and unmerge processor SHALL set
-   `HEADER` to ` * packages merged and unmerged:` followed by an empty line,
-   `TRAILER` to an empty string.

*   related to: R-PROCESSOR-API-002

# R-PROCESSOR-MERGE-UNMERGE-003: Callbacks #
The list merge and unmerge processor SHALL retrieve the callbacks of the list merge and list unmerge processors and add them to its own callbacks.

*   related to: R-PROCESSOR-API-003
