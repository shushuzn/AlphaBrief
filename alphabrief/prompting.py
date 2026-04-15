"""Prompt rendering helpers."""

from pathlib import Path


def build_final_prompt(report_text: str, template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    return template.replace("{{REPORT_CONTENT}}", report_text)
