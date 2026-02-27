# AlphaBrief

轻量级研报摘要工作流仓库（面向“研报文本 → 结构化总结 Prompt”）。

## 教程目标

本教程帮助你在 5 分钟内完成：

1. 准备一份研报纯文本；
2. 运行 `run_agents.py` 执行分块与中间摘要；
3. 获取可直接投喂给 Research Summary Agent 的最终 Prompt；
4. 自动读取 `agents.md` 显示当前里程碑与 gate；
5. 使用输出末尾的 Compliance Guard 清单做合规复核。

---

## 一、环境准备

### 1) 进入仓库

```bash
cd /workspace/AlphaBrief
```

### 2) 检查 Python

```bash
python3 --version
```

建议 Python 3.10+。

---

## 二、最短可用路径（Quick Start）

### 第 1 步：准备输入文本

将研报内容保存为纯文本文件，例如：`sample_report.txt`。

### 第 2 步：运行默认命令

```bash
python3 run_agents.py --input sample_report.txt
```

你将得到两段核心输出：

- `# Research Summary Agent Prompt`：可直接给总结模型；
- `# Compliance Guard Checklist`：上线前合规检查项。

---

## 三、参数教程（按场景选）

### 场景 A：报告超长，容易超上下文

```bash
python3 run_agents.py \
  --input sample_report.txt \
  --max-chars 50000 \
  --chunk-size-words 3000 \
  --summary-max-words 300
```

说明：
- `--max-chars`：超过该字符数才触发分块；
- `--chunk-size-words`：每个 chunk 的词数；
- `--summary-max-words`：每个 chunk 中间摘要保留词数上限。

### 场景 C：指定 agent 规范文件

```bash
python3 run_agents.py \
  --input sample_report.txt \
  --agents-spec SKILL.md
```

说明：
- `--agents-spec` 用于指定运行时读取的 Agent 规范/skill 文件（默认 `SKILL.md`，若缺失回退 `agents.md`）；
- 程序会输出当前里程碑与 gate，用于将执行行为与规范对齐。

### 场景 B：替换提示词模板

```bash
python3 run_agents.py \
  --input sample_report.txt \
  --template prompts/research_agent.txt
```

说明：
- `--template` 用于指定自定义模板路径；
- 模板中必须包含 `{{REPORT_CONTENT}}` 占位符。

---

## 四、输出解读教程

程序启动后会先输出：

- `# Agents Spec Context`
  - `Source`
  - `Current milestone`
  - `Active gates`

用于把运行时行为和 `agents.md` 规范直接关联。

当输入超出阈值时，还会出现：

- `# Chunking Agent Output`
  - `Chunk count`
  - `Chunk summaries generated`

这表示流程已进入“分块 → 分块摘要 → 合并摘要 → 最终 Prompt”闭环。

---

## 五、常见问题（Troubleshooting）

### 1) 退出码 `2`

通常是参数或输入内容问题：
- `--summary-max-words`、`--chunk-size-words` 非正数；
- `--max-chars` 为负数；
- 输入文件为空文本。

### 1.5) 无空格长文本（如 OCR/CJK）怎么处理？

当前分块器会在无法按空白分词时，自动回退为按字符分块；
并在中间摘要阶段启用字符级压缩，避免合并后再次超限。

### 2) 退出码 `3`

通常是 I/O 问题：
- 输入文件不存在/不可读；
- 模板文件不存在/不可读；
- 文件编码无法按 UTF-8 读取。

---

## 六、模块结构（便于二次开发）

- `alphabrief/chunking.py`：分块与分块摘要
- `alphabrief/workflow.py`：阈值判断、分块编排、摘要合并
- `alphabrief/prompting.py`：模板渲染
- `run_agents.py`：CLI 入口

---

## 七、验证命令

```bash
pytest -q
```

如测试通过，可按当前输出进入下游总结/合规流程。
