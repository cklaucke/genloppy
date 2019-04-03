# R-PARSER-PMS-001: Provide regular expressions according to Gentoo Package Manager Specification #
*genloppy* SHALL provide necessary regular expressions according to [Gentoo Package Manager Specification](https://dev.gentoo.org/~ulm/pms/head/pms.html).

# R-PARSER-PMS-002: Base pattern #
The following base pattern SHALL be used:
-   category: `([A-Za-z0-9_][A-Za-z0-9+_.-]*)` (referred as `{category}`)
-   package name: `([A-Za-z0-9_][A-Za-z0-9+_-]*)` (referred as `{package_name}`)
-   atom base: `{category}/{package_name}` (referred as `{atom_base}`)
-   atom version (cannot stand alone): `(?=-[0-9])-([^\s]+)` (referred as `{atom_version}`)
-   atom: `{atom_base}{atom_version}` (referred as `{atom}`)
-   timestamp: `([0-9]+)` (referred as `{timestamp}`)
-   count: `\(([0-9]+) of ([0-9]+)\)` (referred as `{count}` where the first part is `count_n` and the second part `count_m`)
-   repository name: `([A-Za-z0-9_][A-Za-z0-9_-]*)` (referred as `{repo_name}`)

# R-PARSER-PMS-003: merge begin pattern #
The *merge begin* pattern SHALL use the following regular expression
```
^{timestamp}:  >>> emerge {count} {atom} to .*$
```
The following tokens shall be extracted:
-   `timestamp`,
-   `count_n`
-   `count_m`,
-   `atom`,
-   `atom_base`,
-   `category`,
-   `package_name`,
-   `atom_version`.

# R-PARSER-PMS-004: merge end pattern #
The *merge end* pattern SHALL use the following regular expression
```
^{timestamp}:  ::: completed emerge {count} {atom} to .*$
```
The following tokens shall be extracted:
-   `timestamp`,
-   `count_n`
-   `count_m`,
-   `atom`,
-   `atom_base`,
-   `category`,
-   `package_name`,
-   `atom_version`.

# R-PARSER-PMS-005: unmerge pattern #
The *unmerge* pattern SHALL use the following regular expression
```
^{timestamp}:  >>> unmerge success: {atom}$
```
The following tokens shall be extracted:
-   `timestamp`,
-   `atom`,
-   `atom_base`,
-   `category`,
-   `package_name`,
-   `atom_version`.

# R-PARSER-PMS-006: sync pattern #
The *sync* pattern SHALL use the following regular expression
```
^{timestamp}: === Sync completed for {repo_name}$
```
The following tokens shall be extracted:
-   `timestamp`,
-   `repo_name`.

# R-PARSER-PMS-007: emerge log file entries mapping #
*genloppy* SHALL provide a mapping for emerge log file entries:
-    entry `merge_begin` using the *merge begin* pattern,
-    entry `merge_end` using the *merge end* pattern,
-    entry `unmerge` using the *unmerge* pattern,
-    entry `sync` using the *sync* pattern.

# R-PARSER-PMS-008: pretend pattern #
The *sync* pattern SHALL use the following regular expression
```
^\[e[^]]+\] {atom}
```
(Do not match the end of the line, since additional output may following depending on the `emerge` command line switches, e.g. `-v`!)

The following tokens shall be extracted:
-   `atom_base`,
-   `category`,
-   `package_name`,
-   `atom_version`.

Note: The bracket part of the regular expression for pretended packages was taken from the original implementation of `genlop`. The `e[^]]+` will most likely match `ebuild` and not  `blocks`, `nomerge` etc. This may lead to inaccurate results if the pretend output contains blockers (a warning may be helpful for the user). According to the manpage of `emerge`, `e[^]]+` shall suffice.

# R-PARSER-PMS-009: emerge pretend entries mapping #
*genloppy* SHALL provide a mapping for emerge pretend entries:
-    entry `pretended_package` using the *pretend* pattern.
