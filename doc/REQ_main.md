# R-MAIN-001: Provide main function #
*genloppy* SHALL provide a main function.

# R-MAIN-002: Main class execution #
The main function SHALL
1. parse arguments and determine the configuration to use,
2. setup the desired processor using the configuration and the given output handler,
3. setup the parser for emerge logs using the configuration and subscribe the callbacks retrieved from the processor,
5. configure the output handler,
6. do the processor's pre-processing,
7. let the parser for emerge logs parse `/var/log/emerge.log`,
8. do the processor's post-processing.
