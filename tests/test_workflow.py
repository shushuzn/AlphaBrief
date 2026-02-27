from pathlib import Path

from alphabrief.chunking import split_words, summarize_chunk
from alphabrief.prompting import build_final_prompt
from alphabrief.workflow import prepare_workflow


def test_split_words_returns_empty_on_blank_input():
    assert split_words("   ", 5) == []


def test_split_words_respects_chunk_size():
    text = "one two three four five"
    assert split_words(text, 2) == ["one two", "three four", "five"]


def test_summarize_chunk_truncates_and_marks_ellipsis():
    text = "one two three four"
    assert summarize_chunk(text, 2) == "one two ..."


def test_prepare_workflow_no_chunking_on_threshold_boundary():
    text = "abcd"
    result = prepare_workflow(text, max_chars=len(text), chunk_size_words=2, summary_max_words=2)
    assert result.chunks == []
    assert result.chunk_summaries == []
    assert result.merged_text == text


def test_prepare_workflow_chunking_generates_summaries_when_over_threshold():
    text = "one two three four"
    result = prepare_workflow(text, max_chars=3, chunk_size_words=2, summary_max_words=1)
    assert len(result.chunks) == 2
    assert len(result.chunk_summaries) == 2
    assert "[CHUNK SUMMARY 1]" in result.merged_text
    assert "[CHUNK SUMMARY 2]" in result.merged_text


def test_build_final_prompt_replaces_placeholder(tmp_path: Path):
    template = tmp_path / "template.txt"
    template.write_text("prefix\n{{REPORT_CONTENT}}\nsuffix", encoding="utf-8")
    rendered = build_final_prompt("hello", template)
    assert rendered == "prefix\nhello\nsuffix"
