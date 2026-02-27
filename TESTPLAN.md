# TESTPLAN (M1)

## Definition of Done
- CLI 执行时会读取 `agents.md` 并输出当前里程碑与 gate 信息。
- 缺失 `agents.md`（或自定义 `--agents-spec` 文件）时返回 I/O 错误退出码 `3`。
- 现有 workflow/CLI 测试保持通过。

## Acceptance Tests
- **T1**: CLI 输出包含 `# Agents Spec Context`、`Current milestone`、`Active gates`。
- **T2**: `--agents-spec` 指向不存在文件时返回 exit code `3`。
- **T3**: `pytest -q` 全量通过。

## Command
- `pytest -q`
