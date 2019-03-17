# R-PARSER-ENTRY-HANDLER-001: Provide a handler for emerge log entry events #
*genloppy* SHALL provide a handler for emerge log entry events.

# R-PARSER-ENTRY-HANDLER-002: Entry types #
The initializer SHALL take `entry_types` to set available entry types.

# R-PARSER-ENTRY-HANDLER-003: Provide an API to register entry event listeners #
The handler SHALL provide a method `register_listener` which takes
-   a callable `callback` (which takes a `properties` dictionary) and
-   optionally an `entry_type` to register for.

If the `entry_type` is not given, `register_listener` SHALL register the given `callback` for all available entry types. Otherwise `callback` SHALL be registered for the given `entry_type`.

If the given `entry_type` does not exist, `register_listener` SHALL raise a `RuntimeError`.

# R-PARSER-ENTRY-HANDLER-004: Provide a callback for entry events #
The handler SHALL provide a callback for entry events named `entry`. It SHALL take
-   `entry_type`: the type of the entry and
-   `properties`: a dictionary of key-value pairs.

`entry` SHALL call every `callback` listening for the given `entry_type` passing the `properties` dictionary.
