# TESTPLAN (M1)

## Definition of Done
- System handles long text input by chunking without crashing.
- Over-threshold input is transformed as chunk summaries and merged before final prompt.
- Output contains required prompt and compliance checklist sections.
- Missing/invalid input is reported with clear non-zero exit code.

## Acceptance Tests
- **T1**: Over-threshold report text triggers chunking and chunk-summary generation, then completes successfully.
- **T2**: CLI output includes `# Research Summary Agent Prompt` and `# Compliance Guard Checklist`.
- **T3**: Empty input fails with exit code `2`; workflow preprocessing does not fabricate missing report facts.

## Command
- `pytest -q`
