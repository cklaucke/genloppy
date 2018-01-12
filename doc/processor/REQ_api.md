# R-PROCESSOR-API-001: Provide an API for item processing #
*genloppy* SHALL provide an API for processing items.

# R-PROCESSOR-API-002: Provide a pre-processing interface #
The processor API SHALL provide a method for pre-processing. The method SHALL be named `pre_process`.

# R-PROCESSOR-API-003: Provide an interface for retrieving callbacks to be subscribed #
The processor API SHALL provide a method returning a dict of modes and associated callbacks to be subscribed. The method SHALL be named `callbacks`.

# R-PROCESSOR-API-004: Provide a post-processing interface #
The processor API SHALL provide a method for post-processing. The method SHALL be named `post_process`.
