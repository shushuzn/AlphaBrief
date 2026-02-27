# Changelog

## [0.1.2] - 2026-02-27
### Added
- Added intermediate chunk-summary generation (`summarize_chunk`) to create a closed chunking pipeline for long reports.
- Added CLI option `--summary-max-words` to control summary compression per chunk.
- Expanded tests to cover chunk-summary behavior and long-input CLI flow.

### Changed
- Updated workflow orchestration to merge chunk summaries (instead of raw chunks) into final prompt input.
- Updated milestone artifacts and docs to reflect chunk-summary merge stage.
