# R-PROCESSOR-PRETEND-001: Provide a pretend processor implementation #
*genloppy* SHALL provide a pretend processor implementation.
The pretend processor SHALL be subclassed from base output processor.

# R-PROCESSOR-PRETEND-002: Header and trailer #
The pretend processor SHALL set
-   `HEADER` to `These are the pretended packages: (this may take a while; wait...)` followed by an empty line,
-   `TRAILER` to `Estimated update time: {}.`, where the placeholder SHALL be replaced by the calculated estimated update time.

*   related to: R-PROCESSOR-BASE-OUTPUT-001

# R-PROCESSOR-PRETEND-003: Pre-process implementation #
In addition to the default implementation the pretend processor SHALL use the `tokenizer` configured with emerge pretend entries mapping and an `entry handler` to collect all pretended packages from the output of an `emerge -p` or `emerge --pretend` command.

*   related to: R-PROCESSOR-API-003
*   depends on: R-PARSER-TOKENIZER-001
*   depends on: R-PARSER-ENTRY-HANDLER-001
*   depends on: R-PARSER-PMS-008

# R-PROCESSOR-PRETEND-004: Callbacks #
The pretend processor SHALL use and instance of the duration processor initialized with callback `process`.
It SHALL retrieve the callbacks of the duration processor and add them to its own callbacks.

*   related to: R-PROCESSOR-API-003
*   depends on: R-PROCESSOR-DURATION-001

# R-PROCESSOR-PRETEND-005: process callback implementation #
The callback SHALL store the `duration` for `atom_base`.

# R-PROCESSOR-PRETEND-006: Post-process implementation #
The pretend processor SHALL *override* the default implementation. It SHALL
-   estimate the total duration of the pretend output by adding the average of the merge durations for all pretended packages,
-   pretty print the estimated update time in a human-readable way using `TRAILER`.

If no merge duration is available for a pretended package, a warning message SHALL be printed.

*   related to: R-PROCESSOR-API-004
