# R-OUTPUT-API-001: Provide an API for output operations #
*genloppy* SHALL provide an API for output operations.

# R-OUTPUT-API-003: Configure output #
The output API SHALL provide a method to configure the output. The method SHALL be named `configure` and take optional keyword arguments.

# R-OUTPUT-API-003: Message output #
The output API SHALL provide a method to output a message. The method SHALL be named `message` and take one argument:
-   the message to be outputted.

# R-OUTPUT-API-004: Merge item output #
The output API SHALL provide a method to output a merge item. The method SHALL be named `merge_item` and take three arguments:
-   the timestamp,
-   the atom's name,
-   the atom's version.


# R-OUTPUT-001: Provide an configurable output implementation #
*genloppy* SHALL provide a configurable output implementation.

# R-OUTPUT-002: Implement output API #
The output implementation SHALL realize the output API.

*   related to: R-OUTPUT-API-001

# R-OUTPUT-003: Allow for configuration of colored output #
The output implementation SHALL allow for configuration the output color:
-   colored, or
-   uncolored.

# R-OUTPUT-004: Allow for configuration of timezone to use for dates #
The output implementation SHALL allow for configuration the timezone to use for displaying dates:
-   local timezone, or
-   Coordinated Universal Time (UTC) (-> legacy Greenwich Mean Time (GMT)).

# R-OUTPUT-005: Date formatting #
The output implementation SHALL print dates as specified by the current locale.

If UTC was configured, dates SHALL be printed in Coordinated Universal Time.
Otherwise, dates SHALL be printed in local time.

# R-OUTPUT-006: Message output #
The output implementation SHALL print the message as given.

*   related to: R-OUTPUT-API-003

# R-OUTPUT-007: Merge item output #
The output implementation SHALL print
1. five (5) spaces
2. the timestamp as formatted date
3. the separator `>>>` preceded and succeeded by a space
4. the atom's name and version separated by a `-`

Ex.
```
     Thu Nov 23 01:43:04 2017 >>> sys-devel/gcc-6.4.0
```

*   related to: R-OUTPUT-API-004