# R-CONF-CLI-001: Configuration through command line interface #
*genloppy* SHALL provide a command line interface.


# R-CONF-CLI-002: Positional argument #
The command line interface SHALL provide a positional argument `name` which SHALL be optional and allowed to be specified repeatedly.


# R-CONF-CLI-003: Sub-command arguments #
The command line interface SHALL provide

*   a sub-command argument `-h`/`--help` which displays help information,

*   a sub-command argument `-i`/`--info` which prints a brief summary of the currently installed packages (USE, CFLAGS, CXXFLAGS, LDFLAGS, average and total build time). This flag requires at least one `name` or `-s`/`--search` to be given,

*   a sub-command argument `-l`/`--list` which prints the history of merges. This flag optionally accepts `name` and/or `-s`/`--search`,

*   a sub-command argument `-r`/`--rsync` which prints the history of syncs. This flag does not allow a `name` or `-s`/`--search` to be given,

*   a sub-command argument `-t`/`--time` which calculates and prints the merge time. This flag requires at least one `name` or `-s`/`--search` to be given,

*   a sub-command argument `-u`/`--unmerge` which prints the history of unmerges. This flag optionally accepts `name` and/or `-s`/`--search`,

*   a sub-command argument `-p`/`--pretend` which prints a merge time estimation for the output of `emerge -p`. This flag does not allow a `name` or `-s`/`--search` to be given,

*   a sub-command argument `-c`/`--current` which prints a merge time estimation for an ongoing merge. This flag does not allow a `name` or `-s`/`--search` to be given,

*   a sub-command argument `-v`/`--version` which prints the version information.


# R-CONF-CLI-004: Key-value option arguments #
The command line interface SHALL provide

*   a key-value option argument `-f` which takes a filename as value and SHALL be allowed to be specified repeatedly,

*   a key-value option argument `-s`/`--search` which takes a regular expression as value to be used for package searches and SHALL be allowed to be specified repeatedly,

*   a key-value option argument `--date` which takes a date specification as value and SHALL be allowed to be specified up to two times. The value of the first occurrence of `--date` SHALL be taken as start date. The value of the second occurrence SHALL be taken as end date. The output SHALL be limited to log entries between start date and end date.


# R-CONF-CLI-005: Flag arguments #
The command line interface SHALL provide

*   a flag argument `-g`/`--gmt` which sets the display time format to GMT/UTC.

*   a flag argument `-n`/`--nocolor` which disables the colored output,

*   a flag argument `-q` which queries the gentoo.linuxhowtos.org database if no local emerge was found. This flag requires at least one `name` or `-s`/`--search` to be given.

*   a flag argument `-S` which enables case sensitive matching.


# R-CONF-CLI-006: Check parsed arguments #
The command line interface SHALL provide means to check the parsed arguments.

The following rules SHALL be checked:
-   only specified arguments are given
-   key-value arguments are provided with a value
-   admissible count of date (R-CONF-CLI-004) arguments
-   exactly one sub-command (R-CONF-CLI-003) SHALL be given with one exception:
    -   merge and unmerge history MAY BE given at the same time
-   query flag (R-CONF-CLI-005) SHALL only be allowed for sub-commands (R-CONF-CLI-003): current, pretend, time
-   if constrained, name (R-CONF-CLI-002) and search (R-CONF-CLI-004) SHALL fulfill the sub-command's requirements

If at least one rule is not fulfilled the argument check SHALL raise an exception.


# R-CONF-CLI-007: Configuration from parsed arguments #
The command line interface SHALL provide means to get the configuration from the parsed arguments.

It SHALL provide:
*   the given names
*   the name of the corresponding processor for the given sub-commands
*   the given filenames
*   the given dates preserving the given order
*   the given regular expressions to search for
*   the given flags gmt, nocolor, query and case sensitiveness
