# R-PARSER-ELOG-001: Provide parser for emerge logs #
*genloppy* SHALL provide a parser for emerge logs.

# R-PARSER-ELOG-002: Utilize regular expressions and callbacks #
The parser SHALL use regular expressions for parsing the emerge log. Each regular expression is associated with a callback taking the match as argument.

# R-PARSER-ELOG-003: Parser input and modes #
The parser SHALL provide a parse method which takes
-   a file-like object as input and
-   a parser mode.

The following parser modes SHALL be available:
-   *merge* mode
-   *unmerge* mode
-   *sync* mode
-   special mode *any* which takes all modes mentioned above into consideration (default)

The parse method SHALL iterate through the lines of the given file-like object matching the patterns determined by the given parser mode. If a pattern matches it SHALL invoke the associated callback. If the callback returns an item, the parse method SHALL yield that return value to the caller.

The parse method SHALL raise an exception if more than one regular expression matches for a single line.

# R-PARSER-ELOG-004: Mode merge #
The parser SHALL parse *merges*. A *merge* is a "stateful" entry.
The parser SHALL look for *merge begin* using the following pattern
```
???
```
If the pattern matches, the associated callback SHALL save timestamp, atom base, atom version and count.

Furthermore, the parser SHALL look for *merge end* using the following pattern
```
???
```
If the pattern matches, the associated callback SHALL check against the saved values atom base, atom version and count from *merge begin*. If they match, the callback SHALL return a *MergeItem* initialized with the timestamps of merge begin and merge end, the atom base and the atom version. Otherwise the entry SHALL be ignored.

The parser SHALL always look for both patterns. The following inconsistencies SHALL be ignored:
-   merge begin without a merge end,
-   merge end without a merge begin.

# R-PARSER-ELOG-005: Mode unmerge #
The parser SHALL parse *unmerges*. The parser SHALL look for *unmerge* using the following pattern
```
???
```
If the pattern matches, the associated callback SHALL return an *UnmergeItem* initialized with the timestamp, the atom base and the atom version.

# R-PARSER-ELOG-006: Mode sync #
The parser SHALL parse *syncs*. The parser SHALL look for *sync* using the following pattern
```
???
```
If the pattern matches, the associated callback SHALL return a *SyncItem* initialized with the timestamp and the repository name.
