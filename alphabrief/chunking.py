"""Chunking utilities for long report processing."""


def split_words(text: str, chunk_size: int) -> list[str]:
    """Split text into chunks.

    Primary strategy is word-based splitting. If the input has no whitespace
    boundaries (common in some OCR or CJK extracts), fall back to fixed-size
    character chunks to avoid producing an oversized single block.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    normalized = text.strip()
    if not normalized:
        return []

    words = normalized.split()
    if len(words) > 1:
        return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]

    # Fallback: no reliable whitespace tokenization, chunk by characters.
    source = words[0]
    if len(source) <= chunk_size:
        return [source]

    return [source[i : i + chunk_size] for i in range(0, len(source), chunk_size)]


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
