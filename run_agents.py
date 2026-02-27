#!/usr/bin/env python3
"""Execute the local agents configuration workflow for research reports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alphabrief.prompting import build_final_prompt
from alphabrief.workflow import prepare_workflow

PROMPT_TEMPLATE_PATH = Path("prompts/research_agent.txt")


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute Research Intelligence Agents workflow")
    parser.add_argument("--input", required=True, help="Path to extracted report text file")
    parser.add_argument("--max-chars", type=int, default=120000, help="Max report chars before chunking")
    parser.add_argument("--chunk-size-words", type=int, default=4000, help="Words per chunk")
    parser.add_argument(
        "--summary-max-words",
        type=int,
        default=400,
        help="Maximum words kept in each intermediate chunk summary",
    )
    args = parser.parse_args()

    if args.max_chars < 0 or args.chunk_size_words <= 0 or args.summary_max_words <= 0:
        print(
            "Error: --max-chars must be >= 0, --chunk-size-words and --summary-max-words must be > 0",
            file=sys.stderr,
        )
        raise SystemExit(2)

    report_path = Path(args.input)
    try:
        report_text = report_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"I/O Error: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc

    if not report_text.strip():
        print("Error: input report is empty", file=sys.stderr)
        raise SystemExit(2)

    workflow = prepare_workflow(
        report_text,
        max_chars=args.max_chars,
        chunk_size_words=args.chunk_size_words,
        summary_max_words=args.summary_max_words,
    )

    if workflow.chunks:
        print("# Chunking Agent Output")
        print(f"Chunk count: {len(workflow.chunks)}")
        print(f"Chunk summaries generated: {len(workflow.chunk_summaries)}")
        print("Action: merged chunk summaries are forwarded to final stage.\n")

    final_prompt = build_final_prompt(workflow.merged_text, PROMPT_TEMPLATE_PATH)
    print("# Research Summary Agent Prompt\n")
    print(final_prompt)
    print("\n# Compliance Guard Checklist")
    print("- Remove buy/sell language")
    print("- Remove price target recommendations")
    print("- Remove guaranteed returns")
    print("- Append disclaimer")


if __name__ == "__main__":
    main()
