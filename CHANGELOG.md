# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2023-12-03

### Changed

- add `requirements.txt` for dependency tracking
- fix many ruff and mypy findings
- centralize configuration in `pyproject.toml`
- modernize `tox.ini`
- remove stale files


## [0.2.0] - 2023-12-02

### Changed

- [GH-103] upgrade to tox v4
- modernize code
- unify formatting with black
- introduce and upgrade CI/CD github action
- add a lot of type hints
- use dataclasses wherever possible
- drop support for Python 3.10
- add support for Python 3.12


## [0.1.0] - 2021-05-16

### Added

- [GH-98] print build duration statistics on a per-package basis for pretend (`-p`)
- [GH-88] print minimum and maximum deviation from estimated build time for pretend (`-p`)
- [GH-20] support multiple and compressed log files
- [GH-11] print the merge times for a given package (`-t`)
- [GH-18] filter packages by specified package names and/or search regexes
- [GH-12] estimate the build time from an `emerge --pretend` input (`-p`)
- [GH-7] print list of all syncs (`-r`)
- [GH-33] print list of merges and unmerges (`-lu`)
- [GH-8] print list of unmerges (`-u`)
- [GH-6] print list of merges (`-l`)
- [GH-26] provides command line interface