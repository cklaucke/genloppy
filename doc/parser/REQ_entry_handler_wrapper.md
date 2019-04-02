# R-PARSER-ENTRY-HANDLER-WRAPPER-001: Provide a entry handler wrapper for filtering events #
*genloppy* SHALL provide an entry handler wrapper for filtering emerge log entry events. It SHALL implement the entry handler API.

* depends on: R-PARSER-ENTRY-HANDLER-API-001

# R-PARSER-ENTRY-HANDLER-WRAPPER-002: Wrapping an entry handler #
The entry handler wrapper SHALL take an entry handler for `__call__` and store it and return the wrapper itself.

# R-PARSER-ENTRY-HANDLER-WRAPPER-003: Registering entry event listeners #
The entry handler wrapper SHALL delegate all `register_listener` calls to the wrapped entry handler.

* realizes: R-PARSER-ENTRY-HANDLER-API-002

# R-PARSER-ENTRY-HANDLER-WRAPPER-004: Provide a getter for listener #
The entry handler wrapper SHALL delegate all `listener` calls to the wrapped entry handler.

* realizes: R-PARSER-ENTRY-HANDLER-API-003

# R-PARSER-ENTRY-HANDLER-WRAPPER-005: Provide a predicate API for filtering entry events #
The entry handler wrapper SHALL provide an predicate API for filtering entry events. It SHALL be named `test`.
It SHALL take
-   `properties`: a dictionary of key-value pairs

and return
-   a `boolean`: `True` to use the event; reject otherwise.

# R-PARSER-ENTRY-HANDLER-WRAPPER-006: Provide a callback for entry events #
The callback SHALL evaluate the predicate `test` passing `properties`. If the predicate returned `True` the callback SHALL delegate the call to the wrapped entry handler, otherwise return.

* realizes: R-PARSER-ENTRY-HANDLER-API-004
