"""Helpers to read execution context from agents.md."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


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

    def current_milestone(self) -> MilestoneStatus | None:
        for milestone in self.milestones:
            if milestone.status == "IN_PROGRESS":
                return milestone
        for milestone in self.milestones:
            if milestone.status == "TODO":
                return milestone
        return self.milestones[0] if self.milestones else None


def load_agents_spec(path: Path) -> AgentsSpec:
    text = path.read_text(encoding="utf-8")

    milestone_pattern = re.compile(
        r"- id:\s*(?P<id>\S+)\s*\n\s*name:\s*\"(?P<name>[^\"]+)\"\s*\n\s*status:\s*(?P<status>\S+)",
        re.MULTILINE,
    )
    milestones = [
        MilestoneStatus(m.group("id"), m.group("name"), m.group("status"))
        for m in milestone_pattern.finditer(text)
    ]

    gate_pattern = re.compile(r"- name:\s*\"[^\"]+\"\s*\n\s*rule:\s*\"(?P<rule>[^\"]+)\"", re.MULTILINE)
    gates = [m.group("rule") for m in gate_pattern.finditer(text)]

    return AgentsSpec(source=path, milestones=milestones, gates=gates)
