# Changelog

## [0.1.10] - 2026-02-27
### Added
- Added spec validation (`milestones`, `gates`, `iteration steps`, `repo_artifacts`) in `alphabrief.agents_spec.AgentsSpec.validate`.
- Added CLI test coverage for invalid spec files that must fail fast.

### Changed
- Strengthened skill execution behavior: `run_agents.py` now validates loaded `SKILL.md/agents.md` before processing input.
- CLI context now includes explicit `Mode: skill-driven execution` and iteration loop reporting.
- Updated README for skill-first loading and spec-validation failure semantics.
