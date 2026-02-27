# ResearchFlash Agents (Executable Roadmap)

> 本文件是仓库中 Agent 执行规范的**单一事实来源（SSOT）**。  
> 所有 Agent 在每次迭代都必须遵循本文档。

---

## 0) Operating Protocol（必须遵守）

### 0.1 Mandatory Iteration Loop
每个里程碑或补丁迭代，都必须严格按顺序执行：

1. **Plan**
   - 更新 `TODO.md`（本次迭代任务拆解）
   - 更新 `TESTPLAN.md`（DoD + 验收测试）
2. **Build**
   - 小步实现，仅覆盖当前里程碑范围
3. **Test**
   - 运行 `pytest`（或等效检查）
   - 更新 `TEST_REPORT.md`（记录命令、结果、覆盖关系）
4. **Release**
   - 更新 `CHANGELOG.md`
   - 若里程碑完成：更新 `VERSION` 并生成 `RELEASE_NOTES.md`
   - 在本文档 Roadmap 中同步里程碑状态（`TODO` / `IN_PROGRESS` / `DONE`）

### 0.2 Required Output Artifacts（每轮必产出）
- `TODO.md`
- `TESTPLAN.md`
- `TEST_REPORT.md`
- `CHANGELOG.md`
- `VERSION`

### 0.3 Hard Rules（禁止项）
- 禁止越过当前里程碑范围实现未来功能
- 禁止在未修改本文件的情况下变更路线图
- 禁止省略测试记录与发布记录

---

## 1) Agent Roles

### 1.1 Research Summary Agent
**Role:** 将研报文本转换为结构化摘要  
**Input:** 提取后的报告文本  
**Output:** 固定章节（Core Viewpoints / Earnings / Logic / Risks / 300-word）  
**Constraints:** 禁止投资建议、禁止股价预测、禁止编造事实

### 1.2 Chunking Agent
**Role:** 对长文档分块并生成块级摘要

### 1.3 Compliance Guard Agent
**Role:** 审查并清除建议性措辞，补充免责声明

### 1.4 Release Manager Agent（Meta）
**Role:** 强制执行迭代闭环，维护工件一致性与可追溯性

---

## 2) Executable Roadmap (Machine-Readable)

> Agent 必须按里程碑顺序执行，不得跳跃。

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
    status: IN_PROGRESS
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
```

---

## 3) Definition of Ready / Done（执行辅助）

### DoR（开始前）
- 当前里程碑范围在 `TODO.md` 中已拆解
- 验收测试在 `TESTPLAN.md` 可执行

### DoD（完成时）
- 功能仅覆盖当前里程碑范围
- 验收测试通过并记录在 `TEST_REPORT.md`
- 发布信息已写入 `CHANGELOG.md`
- 版本信息与里程碑状态一致
