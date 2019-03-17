# R-PARSER-ELOG-001: Provide parser for emerge logs #
*genloppy* SHALL provide a parser for emerge logs.

# R-PARSER-ELOG-002: Use an entry handler #
The parser SHALL take an entry handler to delegate entry matches to.

# R-PARSER-ELOG-003: Parsing an emerge log #
The parser SHALL provide a `parse` method which takes
-   a file-like object as input.

The `parse` method SHALL iterate through the lines of the given file-like object matching the entry type patterns.
If a pattern matches `parse` SHALL call the entry handler's `entry` method passing
-   `entry_type`: the entry type,
-   `properties`: a dictionary defined by the entry type.

If an entry handler was not set, `parse` SHALL raise an `EmergeLogParserError`.

# R-PARSER-ELOG-004: Entry type: merge begin #
The parser SHALL parse *merge_begin* entries.
The parser SHALL look for *merge begin* entries using the following regular expression
```
^[0-9]+: {2}>>> emerge \([0-9]+ of [0-9]+\) [a-z0-9-]+/.*(?=-[0-9])-[^\s]+ to .*$
 ^~~~~~ timestamp        ^~~~~~ n  ^~~~~~ m ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
The entry type SHALL be named `merge_begin` and the properties dictionary SHALL consist of
-   `timestamp`,
-   `count_n`
-   `count_m`,
-   `atom_base`,
-   `atom_version`.

# R-PARSER-ELOG-005: Entry type: merge end #
The parser SHALL parse *merge end* entries.
The parser SHALL look for *merge end* entries using the following regular expression
```
^[0-9]+: {2}::: completed emerge \([0-9]+ of [0-9]+\) [a-z0-9-]+/.*(?=-[0-9])-[^\s]+ to .*$
 ^~~~~~ timestamp                  ^~~~~~ n  ^~~~~~ m ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
The entry type SHALL be named `merge_end` and the properties dictionary SHALL consist of
-   `timestamp`,
-   `count_n`
-   `count_m`,
-   `atom_base`,
-   `atom_version`.

# R-PARSER-ELOG-006: Entry type: unmerge #
The parser SHALL parse *unmerge* entries.
The parser SHALL look for *unmerge* entries using the following regular expression
```
^[0-9]+: {2}>>> unmerge success: [a-z0-9-]+/.*(?=-[0-9])-[^\s]+
 ^~~~~~ timestamp                ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
The entry type SHALL be named `unmerge` and the properties dictionary SHALL consist of
-   `timestamp`,
-   `atom_base`,
-   `atom_version`.

# R-PARSER-ELOG-007: Entry type: sync #
The parser SHALL parse *sync* entries.
The parser SHALL look for *sync* entries using the following regular expression
```
^[0-9]+: === Sync completed for .*$
 ^~~~~~ timestamp                ^~ repository name
```
The entry type SHALL be named `sync` and the properties dictionary SHALL consist of
-   `timestamp`,
-   `repo_name`.

# R-PARSER-ELOG-008: Allow for optional configuration of filters #
The parser SHALL provide means to allow for optional configuration of filters.

It SHALL provide at least the following filters:
-   filtering the packages through names,
-   filtering the packages through regular expressions,
-   filtering the date span.

It SHALL be configurable whether the filtering for packages is case-sensitive or not.

# R-PARSER-ELOG-009: Entry types #
The parser SHALL provide a getter which returns all known entry types.
