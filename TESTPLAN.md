# TESTPLAN (M1)

## Definition of Done
- CLI 默认按 skill 文件 (`SKILL.md`) 读取执行规范。
- 当默认 skill 文件缺失时，可回退到 `agents.md`。
- `load_agents_spec` 可直接解析仓库 `SKILL.md`。
- 全量自动化测试通过。

## Acceptance Tests
- **T1**: `tests/test_agents_spec.py` 可成功解析 `SKILL.md` 并识别当前里程碑。
- **T2**: CLI 仍可输出 `Agents Spec Context` 与 gate 信息。
- **T3**: `pytest -q` 全量通过。

## Command
- `pytest -q`
