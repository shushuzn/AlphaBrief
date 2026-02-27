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
