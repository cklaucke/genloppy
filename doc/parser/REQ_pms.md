# R-PARSER-PMS-001: Provide regular expressions according to Gentoo Package Manager Specification #
*genloppy* SHALL provide necessary regular expressions.


# R-PARSER-PMS-002: merge begin pattern #
The *merge begin* pattern SHALL use the following regular expression
```
^[0-9]+: {2}>>> emerge \([0-9]+ of [0-9]+\) [a-z0-9-]+/.*(?=-[0-9])-[^\s]+ to .*$
 ^~~~~~ timestamp        ^~~~~~ n  ^~~~~~ m ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
The following tokens shall be extracted:
-   `timestamp`,
-   `count_n`
-   `count_m`,
-   `atom_base`,
-   `atom_version`.

# R-PARSER-PMS-003: merge end pattern #
The *merge end* pattern SHALL use the following regular expression
```
^[0-9]+: {2}::: completed emerge \([0-9]+ of [0-9]+\) [a-z0-9-]+/.*(?=-[0-9])-[^\s]+ to .*$
 ^~~~~~ timestamp                  ^~~~~~ n  ^~~~~~ m ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
The following tokens shall be extracted:
-   `timestamp`,
-   `count_n`
-   `count_m`,
-   `atom_base`,
-   `atom_version`.

# R-PARSER-PMS-004: unmerge pattern #
The *unmerge* pattern SHALL use the following regular expression
```
^[0-9]+: {2}>>> unmerge success: [a-z0-9-]+/.*(?=-[0-9])-[^\s]+
 ^~~~~~ timestamp                ^~~~~~~~~~~~~ atom base ^~~~~~ atom version
```
The following tokens shall be extracted:
-   `timestamp`,
-   `atom_base`,
-   `atom_version`.

# R-PARSER-PMS-005: sync pattern #
The *sync* pattern SHALL use the following regular expression
```
^[0-9]+: === Sync completed for .*$
 ^~~~~~ timestamp                ^~ repository name
```
The following tokens shall be extracted:
-   `timestamp`,
-   `repo_name`.

# R-PARSER-PMS-006: emerge log file entries mapping #
*genloppy* SHALL provide a mapping for emerge log file entries:
-    entry `merge_begin` using the *merge begin* pattern,
-    entry `merge_end` using the *merge end* pattern,
-    entry `unmerge` using the *unmerge* pattern,
-    entry `sync` using the *sync* pattern.
