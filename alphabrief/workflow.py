"""Workflow orchestration for report preprocessing."""

from dataclasses import dataclass

from .chunking import split_words, summarize_chunk


@dataclass
class WorkflowResult:
    chunks: list[str]
    merged_text: str
    chunk_summaries: list[str]


def prepare_workflow(
    report_text: str,
    max_chars: int,
    chunk_size_words: int,
    summary_max_words: int,
) -> WorkflowResult:
    """Prepare report text for downstream summary agent."""
    if max_chars < 0:
        raise ValueError("max_chars must be non-negative")

    if len(report_text) <= max_chars:
        return WorkflowResult(chunks=[], merged_text=report_text, chunk_summaries=[])

    chunks = split_words(report_text, chunk_size_words)
    chunk_summaries = [summarize_chunk(chunk, summary_max_words) for chunk in chunks]
    merged = "\n\n".join(
        f"[CHUNK SUMMARY {idx + 1}]\n{summary}" for idx, summary in enumerate(chunk_summaries)
    )
    return WorkflowResult(chunks=chunks, merged_text=merged, chunk_summaries=chunk_summaries)
