# TESTPLAN (M1)

## Definition of Done
- 对无空格长文本不再产出单个超长块，能够稳定分块。
- 分块后 workflow 仍能生成 chunk summaries 并合并输出。
- 现有 CLI/workflow 自动化测试全部通过。

## Acceptance Tests
- **T1**: `split_words` 在无空格文本下按字符分块。
- **T2**: `prepare_workflow` 在无空格文本下可完成分块与摘要合并。
- **T3**: `pytest -q` 全量通过。

## Command
- `pytest -q`
