# TESTPLAN (M1)

## Definition of Done
- `agents.md` 明确迭代闭环（Plan/Build/Test/Release）与必产出工件。
- `agents.md` 保留并清晰表达 roadmap 的 gate 与 milestone。
- 文档优化后不破坏现有代码测试通过性。

## Acceptance Tests
- **T1**: `agents.md` 包含 Mandatory Iteration Loop、Required Artifacts、Hard Rules。
- **T2**: `agents.md` roadmap 中 M1 状态更新为 `IN_PROGRESS`，其余里程碑语义保持一致。
- **T3**: `pytest -q` 通过。

## Command
- `pytest -q`
