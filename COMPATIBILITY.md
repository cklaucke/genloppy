# Compatibility to `genlop` #

-   passed dates for date restriction are not checked if the lie in the future (intended behavior: otherwise this would hinder analysis of log files that ran on a system w/ wrong system time or analysis of log files on a system w/ wrong system time )
-   BSD-style options are not supported (supported UNIX short options preceded by a dash and GNU long options preceded by two dashes; in fact `genlop` does not support BSD options; there's a misleading comment in the code)
-   duration output is always the same (first items are separated by comma; last item is separated by "and": `genlop` had two different formats; one for the estimated duration in `pretend / -p` and another for `time / -t`; descriptive durations are *not* supported ("3 days ago" or "less than minute"))
-   if packages and search regex are specified, they are logically ANDed
-   `genlop -e` takes a package (`-e` shows history and is default if any option is used => unintelligible!) but `genlop -l` and `-u` not; => for now `-e` is not supported but may be an alias for `-l`; `-l` and `-u` take package names
-   `-l` and `-u` may be called w/ and w/o a package name (`genlop` doesn't allow call w/ package name)
-   PMS is used throughout the code which may lead to different results since `genlop` doesn't fully rely on PMS
-   currently query is not supported (check if the service is used at all)
-   info consider successful builds only (TODO: log file inconsistencies shall be logged to stderr)
-   `-r` prints syncs (`genlop` doesn't anymore)
-   defaults to default emerge log file if `-f` was not given, otherwise an error is shown if a file specified w/ `-f` was not found (no fallback to default as `genlop` does)
