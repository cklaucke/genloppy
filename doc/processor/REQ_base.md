# R-PROCESSOR-BASE-001: Provide a base processor implementation #
*genloppy* SHALL provide a base processor implementation.

# R-PROCESSOR-BASE-002: Pre-processing implementation #
The base processor SHALL provide a `pre_process` implementation which does nothing.

# R-PROCESSOR-BASE-003: Callbacks implementation #
The base processor SHALL provide a `callbacks` implementation which returns an empty dict.

# R-PROCESSOR-BASE-004: Post-processing implementation #
The base processor SHALL provide a `post_process` implementation which does nothing.

# R-PROCESSOR-BASE-OUTPUT-001: Provide a base output processor implementation #
*genloppy* SHALL provide a base processor implementation that supports output. It SHALL be initialized with an instance of an output implementation named `output`.
