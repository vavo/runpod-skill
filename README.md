# Runpod Codex Skill
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-vavo-5F7FFF?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/vavo) [![Sponsor on GitHub](https://img.shields.io/badge/Sponsor%20on-GitHub-24292F?style=for-the-badge&logo=github)](https://github.com/sponsors/vavo) [![Support on Patreon](https://img.shields.io/badge/Support%20on-Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/vavo)

The most comprehensive Codex skill set for Runpod yet: one practical skill for working across Serverless, Pods, Flash, Public Endpoints, `runpodctl`, MCP, the Python SDK, REST, GraphQL, storage, deployment, and the small operational traps that usually eat the afternoon.

It is built for agents that need to do real Runpod work without pretending yesterday's API fields are still gospel.

## What It Covers

- Serverless workers, handlers, endpoint jobs, local testing, Docker packaging, cold starts, logs, model caching, vLLM, and worker fitness checks.
- Pods, templates, exposed ports, SSH, persistent storage, network volumes, billing/cost guardrails, and `runpodctl` workflows.
- Flash SDK and CLI workflows, including `runpod_flash`, `Endpoint`, local dev, deployment, app environments, custom containers, and storage.
- Public Endpoints model APIs for hosted image, video, audio, and text models, with model-page lookup instead of stale hardcoded catalogs.
- Runpod MCP setup and source-level notes for Codex-compatible infrastructure management.
- Python SDK usage for endpoint requests, worker patterns, and API-key handling.
- REST OpenAPI and GraphQL routing, including the separate GraphQL spec at `https://graphql-spec.runpod.io`.
- A docs helper script that searches and fetches current Runpod documentation from the official docs index.

## Why This Exists

Runpod has a lot of useful surface area, and most agent guidance covers only one slice: a handler example here, a CLI command there, maybe a Dockerfile if the stars are feeling generous. This skill ties the pieces together so Codex can choose the right tool, refresh the right docs, avoid stale assumptions, and keep live infrastructure changes deliberate.

## Install

Copy the `runpod` skill folder into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
rsync -a runpod/ "${CODEX_HOME:-$HOME/.codex}/skills/runpod/"
```

Then invoke it explicitly:

```text
$runpod deploy and troubleshoot this Serverless worker
$runpod check this Dockerfile before I push it to Runpod
$runpod use Public Endpoints to call the current Flux Dev model
```

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
