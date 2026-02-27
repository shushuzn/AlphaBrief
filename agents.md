# ResearchFlash Agents (Executable Roadmap)

This repo is operated by coding agents.  
Agents must follow this file as the single source of truth for iteration, gating, and releases.

---

## 0) Operating Protocol (Must Follow)

### Iteration Loop (Mandatory)
For every iteration (milestone or patch), agents MUST execute:

1. **Plan**
   - Create/Update `TODO.md` with scoped tasks for the next milestone
   - Create/Update `TESTPLAN.md` with acceptance tests
2. **Build**
   - Implement tasks in small commits
3. **Test**
   - Run `pytest` (or relevant checks) locally
   - Record results in `TEST_REPORT.md`
4. **Release**
   - Update `CHANGELOG.md`
   - If milestone completed, update `VERSION` and generate `RELEASE_NOTES.md`
   - Tag the milestone status as `DONE` in the Roadmap section below

### Output Artifacts (Always Produce)
- `TODO.md` (task breakdown for next milestone)
- `TESTPLAN.md` (DoD + acceptance tests)
- `TEST_REPORT.md` (latest run summary)
- `CHANGELOG.md` (human readable)
- `VERSION` (current semantic version: MAJOR.MINOR.PATCH)

### Do Not
- Do not expand scope beyond current milestone
- Do not implement future milestone tasks
- Do not change roadmap without editing this file

---

## 1) Agents

### 1.1 Research Summary Agent
**Role:** Convert report text into structured summary  
**Input:** extracted report text  
**Output:** fixed sections (Core Viewpoints, Earnings, Logic, Risks, 300-word)  
**Constraints:** no investment advice, no price prediction, no fabrication

### 1.2 Chunking Agent
**Role:** split long documents and summarize chunks

### 1.3 Compliance Guard Agent
**Role:** final pass to remove advisory language and append disclaimer

### 1.4 Release Manager Agent (Meta)
**Role:** enforce iteration loop, update artifacts, close milestones  
**Must:** keep repo consistent with roadmap, maintain docs

---

## 2) Executable Roadmap (Machine-Readable)

Agents MUST interpret this roadmap and execute milestones sequentially.

```yaml
project:
  name: ResearchFlash
  version_file: VERSION
  primary_language: python
  runtime: streamlit
  repo_artifacts:
    - TODO.md
    - TESTPLAN.md
    - TEST_REPORT.md
    - CHANGELOG.md
    - RELEASE_NOTES.md
    - VERSION

workflow:
  iteration:
    steps: [plan, build, test, release]
  gates:
    - name: "DoD satisfied"
      rule: "All acceptance tests pass and all required features exist"
    - name: "No advice"
      rule: "Output contains disclaimer and does not include buy/sell/target price language"
    - name: "No hallucination guard"
      rule: "If data not in report, output must say '报告未提及'"

milestones:
  - id: M0
    name: "Demo Baseline"
    status: DONE
    version: "0.1.0"
    dod:
      - "Streamlit app runs"
      - "PDF upload works"
      - "Generates structured summary"
      - "Disclaimer appended"
    deliverables:
      - "app.py"
      - "requirements.txt"
      - ".env.example"

  - id: M1
    name: "Long Report Stability"
    status: TODO
    version: "0.2.0"
    scope:
      - "Chunking for long PDFs"
      - "Chunk summaries merged into final summary"
      - "Hard token/char limits handled gracefully"
    acceptance_tests:
      - id: T1
        desc: "Given 60+ page PDF, system completes without crashing"
      - id: T2
        desc: "Output contains all required sections"
      - id: T3
        desc: "No section invents numbers; missing data => '报告未提及'"
    deliverables:
      - "chunking.py (or equivalent module)"
      - "Updated app.py to use chunking"
      - "TESTPLAN.md updated"

  - id: M2
    name: "Export & History"
    status: TODO
    version: "0.3.0"
    scope:
      - "Export summary to Markdown and DOCX"
      - "Basic local history (store last N summaries)"
    acceptance_tests:
      - id: T4
        desc: "User can download .md file"
      - id: T5
        desc: "User can download .docx file"
      - id: T6
        desc: "History list shows previous runs"
    deliverables:
      - "exporter.py"
      - "storage.py"
      - "UI buttons for export/history"

  - id: M3
    name: "Multi-Report Compare (Pro)"
    status: TODO
    version: "0.4.0"
    scope:
      - "Upload two reports"
      - "Compare viewpoints, forecasts, and risks"
      - "Highlight contradictions"
    acceptance_tests:
      - id: T7
        desc: "Compare output includes: agreement, disagreement, missing"
    deliverables:
      - "compare.py"
      - "Updated UI"

  - id: M4
    name: "Compliance Scanner"
    status: TODO
    version: "0.5.0"
    scope:
      - "Automated scan for advice language"
      - "Block or rewrite unsafe sentences"
      - "Produce compliance report"
    acceptance_tests:
      - id: T8
        desc: "If output contains buy/sell/target, scanner removes or flags"
    deliverables:
      - "compliance.py"
      - "COMPLIANCE_REPORT.md"
