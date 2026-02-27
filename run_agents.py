#!/usr/bin/env python3
"""Execute the local agents configuration workflow for research reports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alphabrief.agents_spec import load_agents_spec
from alphabrief.prompting import build_final_prompt
from alphabrief.workflow import prepare_workflow

DEFAULT_PROMPT_TEMPLATE_PATH = Path("prompts/research_agent.txt")
DEFAULT_AGENTS_SPEC_PATH = Path("SKILL.md")


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
    parser.add_argument(
        "--template",
        default=str(DEFAULT_PROMPT_TEMPLATE_PATH),
        help="Prompt template path (default: prompts/research_agent.txt)",
    )
    parser.add_argument(
        "--agents-spec",
        default=str(DEFAULT_AGENTS_SPEC_PATH),
        help="Agent execution spec path (default: SKILL.md, fallback: agents.md)",
    )
    args = parser.parse_args()

    if args.max_chars < 0 or args.chunk_size_words <= 0 or args.summary_max_words <= 0:
        print(
            "Error: --max-chars must be >= 0, --chunk-size-words and --summary-max-words must be > 0",
            file=sys.stderr,
        )
        raise SystemExit(2)

    requested_spec = Path(args.agents_spec)
    spec_candidates = [requested_spec]
    if requested_spec == DEFAULT_AGENTS_SPEC_PATH:
        spec_candidates.append(Path("agents.md"))

    agents_spec = None
    last_exc: Exception | None = None
    for candidate in spec_candidates:
        try:
            agents_spec = load_agents_spec(candidate)
            break
        except (OSError, UnicodeDecodeError) as exc:
            last_exc = exc

    if agents_spec is None:
        print(f"I/O Error: {last_exc}", file=sys.stderr)
        raise SystemExit(3)

    spec_issues = agents_spec.validate()
    if spec_issues:
        print(f"Error: invalid agents spec ({'; '.join(spec_issues)})", file=sys.stderr)
        raise SystemExit(2)

    report_path = Path(args.input)
    try:
        report_text = report_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
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

    print("# Agents Spec Context")
    print("Mode: skill-driven execution")
    print(f"Source: {agents_spec.source}")
    current = agents_spec.current_milestone()
    if current is not None:
        print(f"Current milestone: {current.milestone_id} ({current.name}) [{current.status}]")
    if agents_spec.gates:
        print("Active gates:")
        for rule in agents_spec.gates:
            print(f"- {rule}")
    if agents_spec.iteration_steps:
        print(f"Iteration loop: {' -> '.join(agents_spec.iteration_steps)}")
    print()

    if workflow.chunks:
        print("# Chunking Agent Output")
        print(f"Chunk count: {len(workflow.chunks)}")
        print(f"Chunk summaries generated: {len(workflow.chunk_summaries)}")
        print(f"Compression rounds: {workflow.compression_rounds}")
        print(f"Truncated to max chars: {workflow.was_truncated}")
        print("Action: merged chunk summaries are forwarded to final stage.\n")

    try:
        final_prompt = build_final_prompt(workflow.merged_text, Path(args.template))
    except (OSError, UnicodeDecodeError) as exc:
        print(f"I/O Error: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc

    print("# Research Summary Agent Prompt\n")
    print(final_prompt)
    print("\n# Compliance Guard Checklist")
    print("- Remove buy/sell language")
    print("- Remove price target recommendations")
    print("- Remove guaranteed returns")
    print("- Append disclaimer")


if __name__ == "__main__":
    main()
