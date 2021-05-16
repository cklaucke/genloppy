# R-PARSER-TOKENIZER-001: Provide a configurable tokenizer #
*genloppy* SHALL provide a configurable tokenizer using regular expressions.

# R-PARSER-TOKENIZER-002: Use an entry handler #
The tokenizer SHALL take an entry handler to delegate entry matches to.

# R-PARSER-TOKENIZER-003: Tokenizer initialization #
The tokenizer SHALL be initialized with
-   a dictionary `entry_type_pattern`: the mapping between entry types and regular expressions to use for tokenizing,
-   an `entry_handler`: the handler used for delegating entry matches,
-   (optionally) an `echo` flag (default `False`): whether matches shall be echoed to the terminal.

# R-PARSER-TOKENIZER-004: Tokenize input #
The parser SHALL provide a `tokenize` method which takes
-   a file-like object as input.

If an entry handler was not given, `tokenize` SHALL raise a `TokenizerError`.

To avoid unnecessary evaluation of regular expressions, `tokenize` SHALL query the `entry_handler` for entries listened to creating a subset of `entry_type_pattern`. If an entry is unknown, `tokenize` SHALL raise a `TokenizerError`.

The `tokenize` method SHALL iterate through the lines of the given file-like object and find line entry matches using the `entry_type_pattern` subset.
If a pattern matches `tokenize` SHALL call the entry handler's `entry` method passing
-   `entry_type`: the entry type,
-   `properties`: a dictionary defined by the entry type.


# R-PARSER-TOKENIZER-005: Allow for optional configuration of filters #
The parser SHALL provide means to allow for optional configuration of filters.

It SHALL provide at least the following filters:
-   filtering the packages through names,
-   filtering the packages through regular expressions,
-   filtering the date span.

It SHALL be configurable whether the filtering for packages is case-sensitive or not.
