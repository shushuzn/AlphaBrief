from pathlib import Path

from alphabrief.agents_spec import load_agents_spec


def test_load_agents_spec_extracts_milestones_and_gates(tmp_path: Path):
    spec_file = tmp_path / "agents.md"
    spec_file.write_text(
        """
project:
  repo_artifacts:
    - TODO.md
workflow:
  iteration:
    steps: [plan, build, test, release]
  gates:
    - name: "DoD"
      rule: "All acceptance tests pass"
milestones:
  - id: M1
    name: "Long Report Stability"
    status: IN_PROGRESS
""",
        encoding="utf-8",
    )

    spec = load_agents_spec(spec_file)

    assert len(spec.milestones) == 1
    assert spec.milestones[0].milestone_id == "M1"
    assert spec.current_milestone() is not None
    assert spec.gates == ["All acceptance tests pass"]
    assert spec.iteration_steps == ["plan", "build", "test", "release"]
    assert spec.artifacts == ["TODO.md"]
    assert spec.validate() == []


def test_load_agents_spec_from_repo_skill_file():
    spec = load_agents_spec(Path("SKILL.md"))
    current = spec.current_milestone()
    assert current is not None
    assert current.milestone_id == "M1"
    assert len(spec.gates) >= 1
    assert spec.validate() == []


def test_agents_spec_validate_detects_missing_sections(tmp_path: Path):
    spec_file = tmp_path / "bad.md"
    spec_file.write_text(
        """
workflow:
  iteration:
    steps: [plan, test]
""",
        encoding="utf-8",
    )
    spec = load_agents_spec(spec_file)
    issues = spec.validate()
    assert "missing milestones" in issues
    assert "missing gates" in issues
    assert "missing repo_artifacts" in issues
    assert any(i.startswith("missing iteration steps") for i in issues)
