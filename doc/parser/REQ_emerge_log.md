# R-PARSER-ELOG-001: Provide parser for emerge logs #
*genloppy* SHALL provide a parser for emerge logs.

# R-PARSER-ELOG-002: Utilize regular expressions and callbacks #
The parser SHALL use regular expressions for parsing the emerge log. Each regular expression is associated with a callback taking the match as argument.

# R-PARSER-ELOG-003: Parsing an emerge log #
The parser SHALL provide a `parse` method which takes
-   a file-like object as input.

The `parse` method SHALL iterate through the lines of the given file-like object matching the patterns which were setup by the subscriptions. If a pattern matches `parse` SHALL invoke the associated callback.

The `parse` method SHALL raise an exception if more than one regular expression matches for a single line.

# R-PARSER-ELOG-004: Mode merge #
The parser SHALL parse *merges*. A *merge* is a "stateful" entry.
The parser SHALL look for *merge begin* using the following pattern
```
^[0-9]+: {2}>>> emerge \([0-9]+ of [0-9]+\) [a-z0-9-]+/.*(?=-[0-9])-[^\s]+ to .*$
 ^~~~~~ timestamp        ^~~~~~ n  ^~~~~~ m ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
If the pattern matches, the associated callback SHALL save timestamp, atom base, atom version and count (n and m).

Furthermore, the parser SHALL look for *merge end* using the following pattern
```
^[0-9]+: {2}::: completed emerge \([0-9]+ of [0-9]+\) [a-z0-9-]+/.*(?=-[0-9])-[^\s]+ to .*$
 ^~~~~~ timestamp                  ^~~~~~ n  ^~~~~~ m ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
If the pattern matches, the associated callback SHALL check against the saved values atom base, atom version and count from *merge begin*. If they match, the callback SHALL return a dictionary with the following items:
-   `timestamp_begin`: timestamp of merge begin,
-   `timestamp_end`: timestamp of merge end,
-   `name`: atom base,
-   `version`: atom version.
Otherwise the entry SHALL be ignored.

The parser SHALL always look for both patterns. The following inconsistencies SHALL be ignored:
-   merge begin without a merge end,
-   merge end without a merge begin.

# R-PARSER-ELOG-005: Mode unmerge #
The parser SHALL parse *unmerges*. The parser SHALL look for *unmerge* using the following pattern
```
^[0-9]+: {2}>>> unmerge success: [a-z0-9-]+/.*(?=-[0-9])-[^\s]+
 ^~~~~~ timestamp                ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
If the pattern matches, the associated callback SHALL return a dictionary with the following items:
-   `timestamp`: timestamp of unmerge,
-   `name`: atom base,
-   `version`: atom version.

# R-PARSER-ELOG-006: Mode sync #
The parser SHALL parse *syncs*. The parser SHALL look for *sync* using the following pattern
```
^[0-9]+: === Sync completed for .*$
 ^~~~~~ timestamp                ^~ repository name
```
If the pattern matches, the associated callback SHALL return a dictionary with the following items:
-   `timestamp`: timestamp of sync,
-   `repo_name`: repository name.

# R-PARSER-ELOG-007: Subscribe interface #
The parser SHALL provide a `subscribe` method which takes
-   a subscriber's callback and
-   a mode.

The following modes SHALL be available:
-   *merge* mode
-   *unmerge* mode
-   *sync* mode.

If a subscriber subscribes to a given mode, `subscribe` SHALL store the subscriber's callback in the subscriptions of the mode and setup the corresponding patterns for the `parse` method.

The `subscribe` method SHALL raise an exception if an unknown mode was provided.

# R-PARSER-ELOG-008: Unsubscribe interface #
The parser SHALL provide an `unsubscribe` method which takes
-   a subscriber's callback and
-   optionally, a mode.

If a subscriber unsubscribes with a mode given, the parser SHALL remove the subscriber's callback from the subscriptions of that mode. Otherwise remove the subscriber's callback from all subscriptions.

If a removed subscription was the last one for a mode, `unsubscribe` SHALL also remove the corresponding patterns for the `parse` method.

The `unsubscribe` method SHALL raise an exception if
-   the given callback was not subscribed to the given mode, or
-   the given callback was not subscribed at all, if no mode was given.

# R-PARSER-ELOG-009: Calling subscriber callbacks #
If a log entry matched for a mode, the parser SHALL notify the mode's subscribers by calling the callback providing the resulting dictionary.

# R-PARSER-ELOG-010: Allow for optional configuration of filters #
The parser SHALL provide means to allow for optional configuration of filters.

It SHALL provide at least the following filters:
-   filtering the packages through names,
-   filtering the packages through regular expressions,
-   filtering the date span.

It SHALL be configurable whether the filtering for packages is case-sensitive or not.
