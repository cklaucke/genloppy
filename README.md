# genloppy: README #

*genloppy* aims to be a drop in replacement for [genlop](https://github.com/gentoo-perl/genlop)

## Overview ##

Taken from *genlop*'s manpage.

*genloppy* shall extract information about emerged ebuilds.

Detailed features include:
-   Nice colorful output.
-   Full Portage merge and unmerge history.
-   Display date, time and build time of every merge.
-   Display total and average build time of selected ebuilds\[s\].
-   Estimate upgrade time.
-   Watching current merge progress.
-   Use alternate portage logfile(s).
-   Compressed logfiles (gzip, bzip2) are supported
-   Match ebuild names using regular expressions.
-   Log corruption detection.
-   Display build specific USE, CFLAGS, CXXFLAGS, and LDFLAGS variables.
-   GMT/UTC or localized time and date.
-   Full portage rsync history.

## Design decisions ##

*genloppy* should support the same syntax and options as *genlop*. Clearly document the differences.

*genloppy* should provide the same output as *genlop*. Not applicable if *genlop*'s output is buggy.

*genloppy* shall use **python3**.
-   [ ] define minor version of **python3**
-   [ ] see if **python2.7** can be supported (use six?; probably not worth the effort since **python2.7** has its last rite end of 2019)

*genloppy* shall buffer parser output only if necessary (e.g. for upgrade time estimation), otherwise parser output shall be processed directly.

### Feature: Nice colorful output ###

Use ansi codes.

### Feature: Full Portage merge and unmerge history. ###

Parse timestamp and atom base and version of merges and unmerges and print them.

Requires chronological sorting of logfile entries if more than one logfile was provided. If timestamp ranges of logfiles are not disjoint, parser output must be buffered and sorted afterwards.

### Feature: Display date, time and build time of every merge. ###

Parse timestamps of merge started and merge completed of the affected atom.
Print date and time and calculate build time from start and completed timestamps them.

Requirements as for full history apply.

### Feature: Display total and average build time of selected ebuilds\[s\]. ###

Same as feature build time, but calculate a grand total and the average of the build time.

### Feature: Estimate upgrade time. ###

1.  Same as feature build time, but buffer parser output.
2.  Parse output of pretended emerge.
3.  Query build time (strategy: average/max/recent/...) of each atom from emerge's output and produce a grand total.

### Feature: Watching current merge progress. ###

1.  Determine which atom is currently merging.
2.  Same as build time, maybe enhanced by strategy-selector as in feature estimate upgrade.

### Feature: Use alternate portage logfile(s). ###

Command line option. Use ArgumentParser.

### Feature: Compressed logfiles (gzip, bzip2) are supported ###

Determine file type and decompress using subprocess, zipfile or ...

### Feature: Match ebuild names using regular expressions. ###

Command line option. Use ArgumentParser.
Possible incompatibility due to different regular expression syntaxes between re and perl's syntax?
Re states "his module provides regular expression matching operations similar to those found in Perl."
=> what does similar mean?

### Feature: Log corruption detection. ###

to be defined / analyze what *genlop* does

### Feature: Display build specific USE, CFLAGS, CXXFLAGS, and LDFLAGS variables. ###

Read from /var/db/pkg.

### Feature: GMT/UTC or localized time and date. ###

Use datetime, time, or ...

### Feature: Full portage rsync history. ###

Show completed syncs.
