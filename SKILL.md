# ResearchFlash Workflow Skill

本文件将 `agents.md` 规范以 skill 方式暴露，供 CLI 与自动化流程默认读取。

## Skill Intent
- 将仓库执行规范（里程碑、gate、工件要求）作为可加载上下文。
- 为 `run_agents.py` 提供默认规范入口。
- 保持与 `agents.md` 语义一致，便于人读与机读统一。

## Source of Truth
- Primary governance file: `agents.md`
- This skill mirrors the executable roadmap for runtime loading.

## Executable Roadmap (Machine-Readable)

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

  - id: M1
    name: "Long Report Stability"
    status: IN_PROGRESS
    version: "0.2.0"

  - id: M2
    name: "Export & History"
    status: TODO
    version: "0.3.0"

  - id: M3
    name: "Multi-Report Compare (Pro)"
    status: TODO
    version: "0.4.0"

  - id: M4
    name: "Compliance Scanner"
    status: TODO
    version: "0.5.0"
```
