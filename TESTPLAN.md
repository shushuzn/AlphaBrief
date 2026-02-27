# TESTPLAN (M1)

## Definition of Done
- 教程可指导用户完成从输入文本到最终 Prompt 输出的完整路径。
- 参数说明覆盖长文本与模板替换两类常见场景。
- 文档明确退出码语义，便于用户自助排障。
- 既有自动化测试保持通过。

## Acceptance Tests
- **T1**: README 包含 Quick Start 与分步执行说明。
- **T2**: README 包含 `--max-chars` / `--chunk-size-words` / `--summary-max-words` / `--template` 使用示例。
- **T3**: README 明确退出码 `2` 和 `3` 的常见原因。
- **T4**: `pytest -q` 通过。

## Command
- `pytest -q`
