from pathlib import Path

from alphabrief.agents_spec import load_agents_spec


def test_load_agents_spec_extracts_milestones_and_gates(tmp_path: Path):
    spec_file = tmp_path / "agents.md"
    spec_file.write_text(
        """
milestones:
  - id: M1
    name: "Long Report Stability"
    status: IN_PROGRESS
workflow:
  gates:
    - name: "DoD"
      rule: "All acceptance tests pass"
""",
        encoding="utf-8",
    )

    spec = load_agents_spec(spec_file)

    assert len(spec.milestones) == 1
    assert spec.milestones[0].milestone_id == "M1"
    assert spec.current_milestone() is not None
    assert spec.gates == ["All acceptance tests pass"]


def test_load_agents_spec_from_repo_skill_file():
    spec = load_agents_spec(Path("SKILL.md"))
    current = spec.current_milestone()
    assert current is not None
    assert current.milestone_id == "M1"
    assert len(spec.gates) >= 1
