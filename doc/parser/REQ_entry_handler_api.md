# R-PARSER-ENTRY-HANDLER-API-001: Provide an API for handling entry events #
*genloppy* SHALL provide an an API for handling entry events.

# R-PARSER-ENTRY-HANDLER-API-002: Provide an API to register entry event listeners #
The entry handler API SHALL provide a method for registering entry event listeners. The method SHALL be named `register_listener`.
The method SHALL take
-   a callable `callback` (which takes a `properties` dictionary) and
-   an `entry_type` to register for.

# R-PARSER-ENTRY-HANDLER-API-003: Provide an API to get listener #
The entry handler API SHALL provide a method for getting the registered listener. The getter SHALL be named `listener`.

# R-PARSER-ENTRY-HANDLER-API-004: Provide an API callback for entry events #
The entry handler API SHALL provide a callback for entry events. It SHALL be named `entry`.
It SHALL take
-   `entry_type`: the type of the entry and
-   `properties`: a dictionary of key-value pairs.
