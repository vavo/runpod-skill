# Runpod Codex Skill
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-vavo-5F7FFF?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/vavo) [![Sponsor on GitHub](https://img.shields.io/badge/Sponsor%20on-GitHub-24292F?style=for-the-badge&logo=github)](https://github.com/sponsors/vavo) [![Support on Patreon](https://img.shields.io/badge/Support%20on-Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/vavo)

The most comprehensive Codex skill set for Runpod yet: one practical skill for working across Serverless, Pods, Flash, Public Endpoints, `runpodctl`, MCP, the Python SDK, REST, GraphQL, storage, deployment, and the small operational traps that usually eat the afternoon.

It is built for agents that need to do real Runpod work without pretending yesterday's API fields are still gospel.

## What It Covers

- Serverless workers, handlers, endpoint jobs, Batch Inference, local testing, Docker packaging, cold starts, logs, model caching, vLLM, and worker fitness checks.
- Pods, templates, exposed ports, SSH, persistent storage, network volumes, billing/cost guardrails, and `runpodctl` workflows.
- Runpod SDK beta workflows for remote GPU functions, app deployment, the `rp` CLI, and runtime behavior, plus migration guidance from legacy Flash.
- Legacy Flash SDK and CLI workflows, including `runpod_flash`, `Endpoint`, local dev, deployment, app environments, custom containers, and storage.
- Public Endpoints model APIs for hosted image, video, audio, and text models, with model-page lookup instead of stale hardcoded catalogs.
- Runpod MCP setup and safe operation notes for Codex-compatible infrastructure management.
- Python SDK usage for endpoint requests, worker patterns, and API-key handling.
- REST API v2 resource management, API v1/GraphQL migration, and GraphQL maintenance, including the separate GraphQL spec at `https://graphql-spec.runpod.io`.
- A docs helper script that searches and fetches current Runpod documentation from the official docs index.

## Why This Exists

Runpod has a lot of useful surface area, and most agent guidance covers only one slice: a handler example here, a CLI command there, maybe a Dockerfile if the stars are feeling generous. This skill ties the pieces together so Codex can choose the right tool, refresh the right docs, avoid stale assumptions, and keep live infrastructure changes deliberate.

## Start Here

This repository is a set of instructions for Codex. It is not a Python package, and you do not run `runpod` as a terminal command.

### 1. Download the skill

If you have not downloaded this repository yet:

```bash
git clone https://github.com/vavo/runpod-skill.git
cd runpod-skill
```

If you already have the repository open, just continue from its folder.

### 2. Install it for Codex

Run this from the repository folder:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/runpod"
rsync -a --exclude '__pycache__/' runpod/ "${CODEX_HOME:-$HOME/.codex}/skills/runpod/"
```

This copies the skill into Codex's local skills folder. It does not create a Runpod account, start a Pod, or use an API key.

### 3. Use it in Codex

Start a new Codex chat, then begin your message with `$runpod` and describe what you want help with. For example:

```text
$runpod help me choose between a Pod and Serverless for this project
$runpod check this Dockerfile before I deploy it to Runpod
$runpod help me call a current Public Endpoint
```

You can ask questions first. The skill will identify the right Runpod product and current documentation before suggesting commands or making changes.

## Repository Layout

```text
runpod/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── doc-map.md
│   ├── flash.md
│   ├── graphql.md
│   ├── pods-cli-api.md
│   ├── public-endpoints.md
│   ├── runpodctl.md
│   ├── sdk.md
│   └── serverless.md
└── scripts/
    └── runpod_docs.py
```

## Docs-First Workflow

The skill intentionally avoids baking in fragile tables for GPU names, model catalogs, pricing, API fields, and CLI flags. Instead it points Codex at current official sources and includes a helper:

```bash
python runpod/scripts/runpod_docs.py search serverless handler
python runpod/scripts/runpod_docs.py search public endpoints models
python runpod/scripts/runpod_docs.py page flash/create-endpoints
python runpod/scripts/runpod_docs.py openapi --output /tmp/runpod-openapi.json
# Use --version v1 for the legacy REST schema.
```

Less stale magic. Fewer expensive surprises.

## Validate

From a machine that has the Codex skill-creator tools available:

```bash
uv run --with pyyaml python /path/to/skill-creator/scripts/quick_validate.py runpod
```

The local build of this skill validated successfully with `quick_validate.py`.

## 📜 License
MIT License - go wild, make cool stuff, just don't blame us if your AI starts writing poetry about toast.

Made with ❤️ and way too much coffee by vavo
