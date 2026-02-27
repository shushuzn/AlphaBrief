# Changelog

## [0.1.3] - 2026-02-27
### Added
- Added `--template` CLI option to allow custom prompt template paths.
- Added CLI tests for invalid arguments, missing input file, and missing template file.

### Changed
- Unified CLI I/O error handling to consistently return exit code `3` for input/template read failures.
- Kept M1 long-report chunk-summary merge flow while hardening error-path behavior.
