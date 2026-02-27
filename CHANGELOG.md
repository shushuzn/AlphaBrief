# Changelog

## [0.1.6] - 2026-02-27
### Added
- Added no-whitespace fallback chunking: when tokenization cannot split by spaces, chunker now falls back to fixed-size character chunks.
- Added tests for non-whitespace chunking and workflow integration.

### Changed
- Updated README tutorial troubleshooting to explain handling for OCR/CJK-style no-whitespace long text.
