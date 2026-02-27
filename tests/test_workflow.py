from pathlib import Path

from alphabrief.chunking import split_words, summarize_chunk
from alphabrief.prompting import build_final_prompt
from alphabrief.workflow import prepare_workflow


def test_split_words_returns_empty_on_blank_input():
    assert split_words("   ", 5) == []


def test_split_words_respects_chunk_size():
    text = "one two three four five"
    assert split_words(text, 2) == ["one two", "three four", "five"]


def test_split_words_falls_back_to_char_chunks_when_no_whitespace():
    text = "甲乙丙丁戊己"
    assert split_words(text, 2) == ["甲乙", "丙丁", "戊己"]


def test_summarize_chunk_truncates_and_marks_ellipsis():
    text = "one two three four"
    assert summarize_chunk(text, 2) == "one two ..."


def test_summarize_chunk_uses_char_cap_without_whitespace():
    text = "甲乙丙丁戊己"
    assert summarize_chunk(text, 2) == "甲乙 ..."


def test_prepare_workflow_no_chunking_on_threshold_boundary():
    text = "abcd"
    result = prepare_workflow(text, max_chars=len(text), chunk_size_words=2, summary_max_words=2)
    assert result.chunks == []
    assert result.chunk_summaries == []
    assert result.merged_text == text
    assert result.compression_rounds == 0
    assert result.was_truncated is False


def test_prepare_workflow_chunking_generates_summaries_when_over_threshold():
    text = "aaaaaaaaaa bbbbbbbbbb cccccccccc dddddddddd eeeeeeeeee ffffffffff gggggggggg hhhhhhhhhh"
    result = prepare_workflow(text, max_chars=80, chunk_size_words=4, summary_max_words=1)
    assert len(result.chunks) == 2
    assert len(result.chunk_summaries) == 2
    assert "[CHUNK SUMMARY 1]" in result.merged_text
    assert "[CHUNK SUMMARY 2]" in result.merged_text


def test_prepare_workflow_chunking_handles_non_whitespace_text():
    text = "甲" * 120
    result = prepare_workflow(text, max_chars=80, chunk_size_words=30, summary_max_words=5)
    assert len(result.chunks) == 4
    assert result.chunks[0] == "甲" * 30
    assert len(result.merged_text) <= 80


def test_prepare_workflow_applies_iterative_compression():
    text = " ".join([f"word{i}" for i in range(200)])
    result = prepare_workflow(text, max_chars=250, chunk_size_words=20, summary_max_words=20)
    assert len(result.chunks) > 0
    assert len(result.merged_text) <= 250
    assert result.compression_rounds > 0 or result.was_truncated


def test_prepare_workflow_last_resort_truncation():
    text = " ".join([f"w{i}" for i in range(600)])
    result = prepare_workflow(text, max_chars=40, chunk_size_words=1, summary_max_words=1)
    assert len(result.merged_text) <= 40
    assert result.was_truncated is True
    assert "[TRUNCATED TO MAX_CHARS]" in result.merged_text


def test_build_final_prompt_replaces_placeholder(tmp_path: Path):
    template = tmp_path / "template.txt"
    template.write_text("prefix\n{{REPORT_CONTENT}}\nsuffix", encoding="utf-8")
    rendered = build_final_prompt("hello", template)
    assert rendered == "prefix\nhello\nsuffix"
