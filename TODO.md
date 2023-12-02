# genloppy: TODO #

## 2023-07-10

* try to get rid of EntryHandlerWrapper (EntryHandler should be sufficient; Interface not really needed): EntryHandler
  should be initialized w/ a Predicate-Type (function/call that returns bool) that returns True/False if a package
  matches
* `properties` shall become a dataclass(es) (maybe w/ Protocol-classes that define which fields are required for an 
  operation); as far as I remember: not all fields are always set in `properties` and not all fields are always
  required
* rename EntryHandler to LogEntryHandler (which make its task more clear and avoids confusion)
* use path-like object where handling paths
* pass configurations as dataclass instead of dict (see main.py's dataclasses.asdict)
* use `ruff` and enable most of the plugins
* use `black` or `ruff` for formatting

## 2018-01-04 - 2019-03-19

*   create requirements and trace them
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
pretend
```
^\[e.*\] (.*?)\/(.*?)(\-[0-9])/
```
unmerge
```
^([0-9]{10})\:  \>\>\> unmerge success: ($pattern.*)
```
sync
```
^(.*?)\: \=\=\= Sync completed
```
