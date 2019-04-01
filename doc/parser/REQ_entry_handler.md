# R-PARSER-ENTRY-HANDLER-001: Provide a entry handler for entry events #
*genloppy* SHALL provide an entry handler for emerge log entry events. It SHALL implement the entry handler API.

* depends on: R-PARSER-ENTRY-HANDLER-API-001

# R-PARSER-ENTRY-HANDLER-002: Registering entry event listeners #
The entry handler SHALL implement a method for registering entry event listeners.

The method SHALL store the listener in a dictionary using `entry_type` as key and `callback` as value.
It SHALL be possible to store multiple callbacks per `entry_type`.

* realizes: R-PARSER-ENTRY-HANDLER-API-002

# R-PARSER-ENTRY-HANDLER-003: Provide a getter for listener #
The entry handler SHALL provide a getter for registered listeners returning the dictionary of listeners.

# R-PARSER-ENTRY-HANDLER-004: Provide a callback for entry events #
The entry handler SHALL implement a callback for entry events.

The callback SHALL call all listeners for the given `entry_type` passing the `properties` dictionary.

* realizes: R-PARSER-ENTRY-HANDLER-API-003
