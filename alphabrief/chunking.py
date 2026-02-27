"""Chunking utilities for long report processing."""


def split_words(text: str, chunk_size: int) -> list[str]:
    """Split text into chunks by word count.

    Args:
        text: Source report text.
        chunk_size: Maximum words per chunk. Must be positive.

    Returns:
        List of chunk strings.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    words = text.split()
    if not words:
        return []

    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]


def summarize_chunk(chunk_text: str, summary_max_words: int) -> str:
    """Create a compact intermediate summary from a chunk.

    This is a deterministic fallback summarizer used in M1 to prevent
    oversized prompts before model-level chunk summarization is introduced.
    """
    if summary_max_words <= 0:
        raise ValueError("summary_max_words must be positive")

    words = chunk_text.split()
    if not words:
        return ""

    if len(words) <= summary_max_words:
        return chunk_text

    kept = " ".join(words[:summary_max_words])
    return f"{kept} ..."
