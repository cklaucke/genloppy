# R-PARSER-ENTRY-HANDLER-001: Provide a entry handler for entry events #
*genloppy* SHALL provide an entry handler for emerge log entry events.

# R-PARSER-ENTRY-HANDLER-002: Provide an API to register entry event listeners #
The entry handler SHALL provide a method `register_listener` which takes
-   a callable `callback` (which takes a `properties` dictionary) and
-   optionally an `entry_type` to register for.

# R-PARSER-ENTRY-HANDLER-003: Provide a getter for listener #
The entry handler SHALL provide a getter for registered listeners.

# R-PARSER-ENTRY-HANDLER-004: Provide a callback for entry events #
The entry handler SHALL provide a callback for entry events named `entry`. It SHALL take
-   `entry_type`: the type of the entry and
-   `properties`: a dictionary of key-value pairs.

`entry` SHALL call every `callback` listening for the given `entry_type` passing the `properties` dictionary.
