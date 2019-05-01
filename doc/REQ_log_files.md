# R-LOG-FILES-001: Log files #
*genloppy* SHALL provide processing of multiple log files.
It shall support
-   plain text log files,
-   log files compressed with gzip,
-   log files compressed with bzip2.
-   log files compressed with lzma.

# R-LOG-FILES-002: Default log file #
If no log files were given the main function SHALL use *portage configuration* to get the system's default emerge log file.

If a `PortageConfigurationError` is risen, catch that error an raise a `RuntimeError` suggesting to specify a log file.

*   depends on: R-PORTAGE-CONFIG-002

# R-LOG-FILES-003: Validate log files #
The given log files SHALL be validated by opening each file utilizing decompression if necessary and read the first line using the *log entry* pattern.

## Error handling ##
If any given log file is not accessible, cannot be decompressed or if the *log entry* pattern does not match a `RuntimeError` SHALL be raised. The error message SHALL contain *all* log files that have errors.

*   depends on: R-PARSER-PMS-010


# R-LOG-FILES-004: Order log files chronologically #
1.  Iterate over all log files. Open each file utilizing decompression if necessary and peek the first line using the *log entry* pattern. Store the `timestamp` token for each file name.
2.  Return the file handles of the log files sorted in ascending order by key `timestamp`.

*   depends on: R-PARSER-PMS-010
