# R-PROCESSOR-API-001: Provide an API for processing log entries #
*genloppy* SHALL provide an API for processing log entries.

# R-PROCESSOR-API-002: Provide a pre-processing interface #
The processor API SHALL provide a method for pre-processing. The method SHALL be named `pre_process`.

# R-PROCESSOR-API-003: Provide a method for registration means #
The processor API SHALL provide a method returning a dict of entry types and associated callbacks to be registered.
The method SHALL be named `callbacks`.

# R-PROCESSOR-API-004: Provide a post-processing interface #
The processor API SHALL provide a method for post-processing. The method SHALL be named `post_process`.
