# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-09

### Added

- Initial public release of RingSort
- CLI command: `ringsort PATH`
- Extension-based file categorization
- Dry run mode with planned operation preview
- Recursive sorting with `--recursive`
- Verbose logging with `--verbose`
- Optional log file output with `--log-file`
- Hash-based duplicate detection
- Safe renaming for filename conflicts
- Cross-platform support for Windows, Linux, and macOS
- Pytest test suite with coverage enforcement
- GitHub Actions CI for Ruff, Mypy, and Pytest

### Changed

- Renamed project branding from `organizer` to `ringsort`
- Simplified CLI from `organizer organize PATH` to `ringsort PATH`

[1.0.0]: https://github.com/ammagicring/ringsort/releases/tag/v1.0.0
