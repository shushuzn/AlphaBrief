# TESTPLAN (M1)

## Definition of Done
- 最终合并输出在所有输入下都不超过 `max_chars`。
- `max_chars` 小于截断标记长度时仍能稳定返回受限输出。
- README 说明 tiny-limit 行为，便于用户预期与排障。
- 全量自动化测试通过。

## Acceptance Tests
- **T1**: `prepare_workflow` 在 `max_chars=5` 等极小值下仍满足长度约束。
- **T2**: `prepare_workflow` 常规长文本压缩/截断路径保持正确。
- **T3**: README 包含极小 `max_chars` 行为说明。
- **T4**: `pytest -q` 全量通过。

## Command
- `pytest -q`
