# TESTPLAN (M1)

## Definition of Done
- 程序默认读取 `SKILL.md` 并可回退 `agents.md`。
- 规范文件缺失关键段落时，CLI 必须失败而非继续执行。
- CLI 正常路径仍输出当前里程碑、gates、iteration loop。
- 全量测试通过。

## Acceptance Tests
- **T1**: `load_agents_spec(...).validate()` 对完整 spec 返回空问题列表。
- **T2**: 无效 spec 触发 `invalid agents spec` 并返回 exit code `2`。
- **T3**: CLI 输出包含 `Mode: skill-driven execution` 与 `Iteration loop`。
- **T4**: `pytest -q` 全量通过。

## Command
- `pytest -q`
