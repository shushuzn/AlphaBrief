# TESTPLAN (M1)

## Definition of Done
- 长文本分块后合并摘要文本可稳定落入 `max_chars` 限制。
- 无空格文本在摘要阶段可执行字符级压缩。
- CLI 可展示 `Compression rounds` 与 `Truncated to max chars`。
- 自动化测试全量通过。

## Acceptance Tests
- **T1**: `prepare_workflow` 在极端长文本下会压缩或截断并满足长度上限。
- **T2**: `summarize_chunk` 在 no-whitespace 文本下按字符上限压缩。
- **T3**: CLI 在 chunking 路径输出压缩轮次与截断标识。
- **T4**: `pytest -q` 全量通过。

## Command
- `pytest -q`
