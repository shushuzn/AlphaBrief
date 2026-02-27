# AlphaBrief

轻量级研报摘要工作流仓库。

## 执行 agents.md

仓库提供了 `run_agents.py` 用于把 `agents.md` 里的流程落地执行：

1. 检查输入文本是否超过 `max_chars`（默认 120,000）；
2. 超长文本按词分块（默认每块 4,000 词）；
3. 生成可直接提交给 Research Summary Agent 的最终 Prompt；
4. 输出 Compliance Guard 检查清单。

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

### 示例

```bash
python3 run_agents.py --input sample_report.txt --max-chars 50000 --chunk-size-words 3000
```

### 测试

```bash
pytest -q
```
