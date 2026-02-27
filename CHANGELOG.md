# Changelog

## [0.1.8] - 2026-02-27
### Added
- Added iterative post-chunk compression in workflow so merged chunk summaries respect `max_chars`.
- Added last-resort truncation guard with `[TRUNCATED TO MAX_CHARS]` marker for extreme edge cases.
- Added observability in CLI output: `Compression rounds` and `Truncated to max chars`.

### Changed
- Improved `summarize_chunk` for no-whitespace text to apply character-level compression fallback.
- Expanded workflow/CLI tests to cover compression and truncation paths.
