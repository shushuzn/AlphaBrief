#!/usr/bin/env python3
"""Execute the local agents configuration workflow for research reports.

This utility operationalizes `agents.md` by:
1. Applying max-length checks.
2. Performing optional chunking for long reports.
3. Emitting ready-to-send prompts for each stage.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


PROMPT_TEMPLATE_PATH = Path("prompts/research_agent.txt")


@dataclass
class WorkflowResult:
    chunks: list[str]
    merged_text: str


def split_words(text: str, chunk_size: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]


def prepare_workflow(report_text: str, max_chars: int, chunk_size_words: int) -> WorkflowResult:
    if len(report_text) <= max_chars:
        return WorkflowResult(chunks=[], merged_text=report_text)

    chunks = split_words(report_text, chunk_size_words)
    merged = "\n\n".join(f"[CHUNK {idx+1}]\n{chunk}" for idx, chunk in enumerate(chunks))
    return WorkflowResult(chunks=chunks, merged_text=merged)


def build_final_prompt(report_text: str) -> str:
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    return template.replace("{{REPORT_CONTENT}}", report_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute Research Intelligence Agents workflow")
    parser.add_argument("--input", required=True, help="Path to extracted report text file")
    parser.add_argument("--max-chars", type=int, default=120000, help="Max report chars before chunking")
    parser.add_argument("--chunk-size-words", type=int, default=4000, help="Words per chunk")
    args = parser.parse_args()

    report_path = Path(args.input)
    report_text = report_path.read_text(encoding="utf-8")

    workflow = prepare_workflow(report_text, args.max_chars, args.chunk_size_words)

    if workflow.chunks:
        print("# Chunking Agent Output")
        print(f"Chunk count: {len(workflow.chunks)}")
        print("Action: summarize each chunk, then merge summaries before final stage.\n")

    final_prompt = build_final_prompt(workflow.merged_text)
    print("# Research Summary Agent Prompt\n")
    print(final_prompt)
    print("\n# Compliance Guard Checklist")
    print("- Remove buy/sell language")
    print("- Remove price target recommendations")
    print("- Remove guaranteed returns")
    print("- Append disclaimer")


if __name__ == "__main__":
    main()
