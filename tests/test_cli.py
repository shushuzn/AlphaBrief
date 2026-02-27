import subprocess
import sys
from pathlib import Path


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "run_agents.py", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_outputs_sections(tmp_path: Path):
    input_file = tmp_path / "report.txt"
    input_file.write_text("this is a short report", encoding="utf-8")

    result = run_cli("--input", str(input_file))

    assert result.returncode == 0
    assert "# Research Summary Agent Prompt" in result.stdout
    assert "# Compliance Guard Checklist" in result.stdout


def test_cli_shows_chunk_summary_stage(tmp_path: Path):
    input_file = tmp_path / "report.txt"
    input_file.write_text("one two three four five six", encoding="utf-8")

    result = run_cli(
        "--input",
        str(input_file),
        "--max-chars",
        "1",
        "--chunk-size-words",
        "2",
        "--summary-max-words",
        "1",
    )

    assert result.returncode == 0
    assert "Chunk summaries generated" in result.stdout
    assert "[CHUNK SUMMARY 1]" in result.stdout


def test_cli_errors_on_empty_input(tmp_path: Path):
    input_file = tmp_path / "report.txt"
    input_file.write_text("   ", encoding="utf-8")

    result = run_cli("--input", str(input_file))

    assert result.returncode == 2
    assert "input report is empty" in result.stderr


def test_cli_errors_on_invalid_args(tmp_path: Path):
    input_file = tmp_path / "report.txt"
    input_file.write_text("valid content", encoding="utf-8")

    result = run_cli("--input", str(input_file), "--summary-max-words", "0")

    assert result.returncode == 2
    assert "summary-max-words" in result.stderr


def test_cli_errors_on_missing_input_file(tmp_path: Path):
    missing = tmp_path / "missing.txt"

    result = run_cli("--input", str(missing))

    assert result.returncode == 3
    assert "I/O Error" in result.stderr


def test_cli_errors_on_missing_template(tmp_path: Path):
    input_file = tmp_path / "report.txt"
    input_file.write_text("this is a short report", encoding="utf-8")
    missing_template = tmp_path / "missing_template.txt"

    result = run_cli("--input", str(input_file), "--template", str(missing_template))

    assert result.returncode == 3
    assert "I/O Error" in result.stderr
