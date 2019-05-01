# R-PORTAGE-CONFIG-001: Provide access to portage configuration #
*genloppy* SHALL provide access to portage configuration.

# R-PORTAGE-CONFIG-002: Retrieve the system's default emerge log file #
Portage configuration SHALL provide a method to retrieve the system's default emerge log file.

First, the log directory SHALL be determined according to the following steps:
  1. Determine environment variable `EMERGE_LOG_DIR` using `portageq` and if not empty use that as log directory.
  2. Otherwise, determine environment variable `EPREFIX`, using `portageq`. Remove all system's directory separators from the left of `EPREFIX` and join the system's directory separator with the stripped `EPREFIX` and `var` and `log` as log directory. If `EPREFIX` cannot be determined a `PortageConfigurationError` SHALL be raised.

Finally, join the determined log directory with `emerge.log`.
