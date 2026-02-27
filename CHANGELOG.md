# Changelog

## [0.1.7] - 2026-02-27
### Added
- Added `alphabrief/agents_spec.py` to parse milestone and gate context from `agents.md`.
- Added CLI option `--agents-spec` to bind runtime behavior to a specific agent spec file.
- Added tests for agent spec parsing and missing `--agents-spec` error handling.

### Changed
- `run_agents.py` now prints `# Agents Spec Context` (source, current milestone, active gates) before workflow output.
- Updated README tutorial to document the new spec-context output and argument.
