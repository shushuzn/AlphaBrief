"""Helpers to read execution context from agents/skill spec files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_ITERATION_STEPS = ["plan", "build", "test", "release"]


@dataclass
class MilestoneStatus:
    milestone_id: str
    name: str
    status: str


@dataclass
class AgentsSpec:
    source: Path
    milestones: list[MilestoneStatus]
    gates: list[str]
    iteration_steps: list[str]
    artifacts: list[str]

    def current_milestone(self) -> MilestoneStatus | None:
        for milestone in self.milestones:
            if milestone.status == "IN_PROGRESS":
                return milestone
        for milestone in self.milestones:
            if milestone.status == "TODO":
                return milestone
        return self.milestones[0] if self.milestones else None

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.milestones:
            issues.append("missing milestones")
        if not self.gates:
            issues.append("missing gates")
        if not self.artifacts:
            issues.append("missing repo_artifacts")

        step_set = {step.lower() for step in self.iteration_steps}
        missing_steps = [step for step in REQUIRED_ITERATION_STEPS if step not in step_set]
        if missing_steps:
            issues.append(f"missing iteration steps: {', '.join(missing_steps)}")
        return issues


MILESTONE_PATTERN = re.compile(
    r"- id:\s*(?P<id>\S+)\s*\n\s*name:\s*(?P<name>\"[^\"]+\"|[^\n]+?)\s*\n\s*status:\s*(?P<status>\S+)",
    re.MULTILINE,
)

GATE_PATTERN = re.compile(r"- name:\s*\"[^\"]+\"\s*\n\s*rule:\s*\"(?P<rule>[^\"]+)\"", re.MULTILINE)

ITERATION_STEPS_PATTERN = re.compile(r"steps:\s*\[(?P<steps>[^\]]+)\]")

ARTIFACT_LINE_PATTERN = re.compile(r"^\s*-\s*(?P<artifact>[A-Za-z0-9_.\-/]+)\s*$", re.MULTILINE)


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        return value[1:-1]
    return value


def _extract_repo_artifacts(text: str) -> list[str]:
    block_pattern = re.compile(r"repo_artifacts:\s*(?P<body>(?:\n\s*-\s*[^\n]+)+)", re.MULTILINE)
    block_match = block_pattern.search(text)
    if not block_match:
        return []
    return [m.group("artifact") for m in ARTIFACT_LINE_PATTERN.finditer(block_match.group("body"))]


def load_agents_spec(path: Path) -> AgentsSpec:
    text = path.read_text(encoding="utf-8")

    milestones = [
        MilestoneStatus(
            m.group("id").strip(),
            _strip_quotes(m.group("name")),
            m.group("status").strip(),
        )
        for m in MILESTONE_PATTERN.finditer(text)
    ]

    gates = [m.group("rule") for m in GATE_PATTERN.finditer(text)]

    steps_match = ITERATION_STEPS_PATTERN.search(text)
    iteration_steps = []
    if steps_match:
        iteration_steps = [part.strip().strip('"').strip("'") for part in steps_match.group("steps").split(",")]

    artifacts = _extract_repo_artifacts(text)

    return AgentsSpec(
        source=path,
        milestones=milestones,
        gates=gates,
        iteration_steps=iteration_steps,
        artifacts=artifacts,
    )
