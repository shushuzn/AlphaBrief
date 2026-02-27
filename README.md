# AlphaBrief

轻量级研报摘要工作流仓库。

## 执行 agents.md

仓库提供了 `run_agents.py` 用于把 `agents.md` 里的流程落地执行：

1. 检查输入文本是否超过 `max_chars`（默认 120,000）；
2. 超长文本按词分块（默认每块 4,000 词）；
3. 对每个分块生成中间摘要并合并；
4. 生成可直接提交给 Research Summary Agent 的最终 Prompt；
5. 输出 Compliance Guard 检查清单。

实现模块位于 `alphabrief/`：
- `alphabrief/chunking.py`
- `alphabrief/workflow.py`
- `alphabrief/prompting.py`

### 使用方式

```bash
python3 run_agents.py --input /path/to/report.txt
```

可选参数：

- `--max-chars`：触发分块的最大字符数（默认 `120000`）
- `--chunk-size-words`：每块词数（默认 `4000`）
- `--summary-max-words`：每个 chunk 中间摘要保留词数上限（默认 `400`）
- `--template`：Prompt 模板路径（默认 `prompts/research_agent.txt`）

### 示例

```bash
python3 run_agents.py --input sample_report.txt --max-chars 50000 --chunk-size-words 3000 --summary-max-words 300 --template prompts/research_agent.txt
```

### 测试

```bash
pytest -q
```
