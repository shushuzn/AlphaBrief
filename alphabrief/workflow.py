"""Workflow orchestration for report preprocessing."""

from dataclasses import dataclass

from .chunking import split_words


@dataclass
class WorkflowResult:
    chunks: list[str]
    merged_text: str


def prepare_workflow(report_text: str, max_chars: int, chunk_size_words: int) -> WorkflowResult:
    """Prepare report text for downstream summary agent."""
    if max_chars < 0:
        raise ValueError("max_chars must be non-negative")

    if len(report_text) <= max_chars:
        return WorkflowResult(chunks=[], merged_text=report_text)

    chunks = split_words(report_text, chunk_size_words)
    merged = "\n\n".join(f"[CHUNK {idx + 1}]\n{chunk}" for idx, chunk in enumerate(chunks))
    return WorkflowResult(chunks=chunks, merged_text=merged)
