# Changelog

## [0.1.1] - 2026-02-27
### Added
- Introduced `alphabrief` package modules for chunking, prompting, and workflow orchestration.
- Added unit tests and CLI integration tests using `pytest`.
- Added iteration artifacts: TODO, TESTPLAN, TEST_REPORT.

### Changed
- Refactored `run_agents.py` to consume package modules.
- Added CLI input validation and consistent exit codes for argument/input and I/O errors.
