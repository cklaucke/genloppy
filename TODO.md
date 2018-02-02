# genloppy: TODO #

*   create requirements and trace them
*   check for compat w/ python3.4 or older (since currently developed w/ python3.5)
*   nosetests against original *genlop* output (problem: some output of *genlop* is buggy)
*   name and prioritize features
*   new feature: add multi-processing strategy for log parser -> split log into chunks -> parallel processing (e.g. option -j*n*)
*   pretend improvement: match slot, major, major.minor, ... (useful for e.g. gtk+2 and gtk+3)
*   pretend improvement: consider most recent merge of pkg
*   new feature: cache results of emerge.log parsing
*   analyze what *genlop* does to check for log corruption
*   add all sync types beside sync and git (*genlop*'s git pattern will not work since the git sync module was obviously refactored)
*   provide alternative command line interface (tool w/ sub-command style like git; set of tools w/ reduced functionality like standard unix tools)

original genlop patterns:
merge begin
```
^([0-9]{10})\:  \>\>\> emerge .*?\) $pattern
```
merge end
```
^([0-9]{10})\:  ::: completed .*?\) $pattern to \/
```
unmerge
```
^([0-9]{10})\:  \>\>\> unmerge success: ($pattern.*)
```
sync
```
^(.*?)\: \=\=\= Sync completed
```
