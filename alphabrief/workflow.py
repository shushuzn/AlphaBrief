"""Workflow orchestration for report preprocessing."""

from dataclasses import dataclass

from .chunking import split_words, summarize_chunk


@dataclass
class WorkflowResult:
    chunks: list[str]
    merged_text: str
    chunk_summaries: list[str]
    compression_rounds: int
    was_truncated: bool


def _merge_summaries(chunk_summaries: list[str]) -> str:
    return "\n\n".join(
        f"[CHUNK SUMMARY {idx + 1}]\n{summary}" for idx, summary in enumerate(chunk_summaries)
    )


def prepare_workflow(
    report_text: str,
    max_chars: int,
    chunk_size_words: int,
    summary_max_words: int,
) -> WorkflowResult:
    """Prepare report text for downstream summary agent.

    When chunking is triggered, this function ensures merged chunk summaries
    also respect the max_chars bound by iteratively compressing summaries.
    """
    if max_chars < 0:
        raise ValueError("max_chars must be non-negative")

    if len(report_text) <= max_chars:
        return WorkflowResult(
            chunks=[],
            merged_text=report_text,
            chunk_summaries=[],
            compression_rounds=0,
            was_truncated=False,
        )

    chunks = split_words(report_text, chunk_size_words)

    current_summary_max_words = summary_max_words
    compression_rounds = 0
    was_truncated = False

    while True:
        chunk_summaries = [summarize_chunk(chunk, current_summary_max_words) for chunk in chunks]
        merged = _merge_summaries(chunk_summaries)

        if len(merged) <= max_chars:
            return WorkflowResult(
                chunks=chunks,
                merged_text=merged,
                chunk_summaries=chunk_summaries,
                compression_rounds=compression_rounds,
                was_truncated=was_truncated,
            )

        if current_summary_max_words == 1:
            break

        current_summary_max_words = max(1, current_summary_max_words // 2)
        compression_rounds += 1

    # Last-resort guard for extremely long multi-chunk labels/metadata.
    ellipsis = "\n\n[TRUNCATED TO MAX_CHARS]"
    keep = max(0, max_chars - len(ellipsis))
    merged = (merged[:keep] + ellipsis) if max_chars > 0 else ""
    was_truncated = True
    return WorkflowResult(
        chunks=chunks,
        merged_text=merged,
        chunk_summaries=chunk_summaries,
        compression_rounds=compression_rounds,
        was_truncated=was_truncated,
    )
