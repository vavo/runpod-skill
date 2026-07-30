#!/usr/bin/env python3
"""Validate repository metadata without making network requests."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    skill = ROOT / "runpod" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        raise SystemExit("runpod/SKILL.md is missing valid YAML front matter")

    front_matter = text.split("\n---\n", 1)[0].removeprefix("---\n")
    metadata = yaml.safe_load(front_matter)
    if not isinstance(metadata, dict) or not metadata.get("name") or not metadata.get("description"):
        raise SystemExit("runpod/SKILL.md front matter needs name and description")

    agent_config = yaml.safe_load((ROOT / "runpod" / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    if not isinstance(agent_config, dict) or not isinstance(agent_config.get("interface"), dict):
        raise SystemExit("runpod/agents/openai.yaml must contain an interface mapping")


if __name__ == "__main__":
    main()
