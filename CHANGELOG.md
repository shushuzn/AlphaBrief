# Changelog

## [0.1.11] - 2026-02-27
### Added
- Added edge-case test for tiny `max_chars` truncation behavior to guarantee strict length bounds.

### Changed
- Fixed truncation fallback in workflow to ensure final merged output never exceeds `max_chars`, even when `max_chars` is smaller than truncation marker length.
- Updated README with tiny-limit (`max_chars`) behavior and troubleshooting guidance.
