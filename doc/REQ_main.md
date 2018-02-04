# R-MAIN-001: Provide main function #
*genloppy* SHALL provide a main function.

# R-MAIN-002: Main class execution #
The main function SHALL
1. parse arguments and determine the configuration to use,
2. setup the desired processor using the configuration,
3. setup the parser for emerge logs using the configuration and subscribe the callbacks retrieved from the processor,
4. do the processor's pre-processing,
5. let the parser for emerge logs parse `/var/log/emerge.log`,
6. do the processor's post-processing.
