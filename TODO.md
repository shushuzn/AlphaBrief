# TODO (Current Milestone: M1 Long Report Stability)

## Scope
- [x] 优化核心流程：对 chunk summary 合并结果增加长度守护，避免二次超限。
- [x] 增强无空格文本摘要逻辑：在 no-whitespace 场景下回退到字符级摘要压缩。
- [x] 在 CLI 输出中增加压缩轮次与是否截断指标，提升可观测性。
- [x] 补充 workflow 与 CLI 测试覆盖压缩/截断路径。

## Out of Scope (Per agents.md)
- Export/history features (M2)
- Multi-report comparison (M3)
- Compliance scanner automation (M4)
