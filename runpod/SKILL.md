---
name: runpod
description: Work with Runpod GPU infrastructure and documentation. Use when Codex needs to create, deploy, manage, debug, or review Runpod Pods, Serverless workers/endpoints, templates, network volumes, Public Endpoints, Flash apps, runpodctl commands, Runpod Python SDK usage, REST/GraphQL API usage, Runpod MCP setup, Docker images for Runpod, endpoint request payloads, logs, billing/cost checks, or Runpod deployment troubleshooting.
---

# Runpod

Use this skill to work against Runpod's current docs and infrastructure patterns without guessing old API shapes. Prefer official Runpod docs and local repo evidence over memory.

## First Pass

1. Identify the target product: Serverless, Pods, Flash, Public Endpoints, network volumes, templates, runpodctl, REST API, GraphQL, MCP, or billing.
2. Check whether the request is read-only or mutating. Do not create, start, stop, delete, resize, or redeploy live Runpod resources unless the user explicitly asked for that action.
3. Discover available tools in this order:
   - Runpod MCP tools, if installed in the current environment.
   - `runpodctl`, if installed locally.
   - REST/GraphQL API via `RUNPOD_API_KEY`, if the user asked for live infrastructure work.
   - Official docs only, if answering or planning.
4. Refresh docs before relying on exact flags, fields, URLs, payload sizes, GPU names, pricing, or rate limits. Use `python scripts/runpod_docs.py search <terms>` or browse `https://docs.runpod.io/llms.txt`.
5. Focus on basic usage first: current docs, commands, endpoint calls, SDK examples, and local repo evidence. Open source repos only when debugging the tool/package itself, checking release behavior, or when the user explicitly asks about the repo.
6. Keep secrets out of files and chat. Use environment variables such as `RUNPOD_API_KEY`; never print token values.

## Product Routing

- Serverless worker code, handlers, endpoint jobs, `/run`, `/runsync`, `/status`, streaming, Dockerfiles, cold starts, model caching, vLLM, or queue/load-balancing behavior: read `references/serverless.md`.
- Flash SDK/CLI, `runpod_flash`, `@Endpoint`, `flash dev`, `flash deploy`, Flash apps, local-code remote execution, or Flash endpoint configuration: read `references/flash.md`.
- Public Endpoints, hosted model APIs, model-specific parameters, image/video/audio/text model calls, Vercel AI SDK provider, or Hub playground-generated requests: read `references/public-endpoints.md`.
- runpodctl command usage, CLI install/config, command groups, shell completion, file transfer, CLI output formats, legacy command migration, the `runpod/runpodctl` repo, or the Homebrew tap: read `references/runpodctl.md`.
   - Pods, SSH, JupyterLab, exposed ports, templates, persistent storage, REST API resource management, MCP setup, or network volumes: read `references/pods-cli-api.md`.
- REST API v2 resource management, beta endpoints, v2 OpenAPI, Pods, Serverless, templates, catalog, billing, or network volumes: read `references/api-v2.md`.
- GraphQL schema/spec, `https://api.runpod.io/graphql`, `gpuTypes`, `cpuTypes`, Pod GraphQL mutations, or legacy project code using GraphQL: read `references/graphql.md`.
- Unsure where a topic lives: read `references/doc-map.md`, then fetch the specific official page.

## Common Workflows

### Build or fix a Serverless worker

1. Inspect the repo first: handler entrypoint, Dockerfile, requirements, local test input, model-loading path, and deployment docs/scripts.
2. Keep heavyweight initialization outside the handler.
3. Validate `job["input"]` or `event["input"]` before starting expensive work.
4. Test locally before image/deploy work when possible:

```bash
python handler.py --test_input '{"input": {"prompt": "hello"}}'
python handler.py --rp_serve_api --rp_log_level DEBUG
```

5. For Docker, prefer small runtime images and `.dockerignore`; use CUDA or framework images only when the workload actually needs them.
6. For model assets, prefer Runpod cached models or network volumes when appropriate instead of blindly baking multi-GB files into every image.

### Send requests to queue-based endpoints

Use the endpoint URL shape `https://api.runpod.ai/v2/{endpoint_id}/...`.

- Use `/runsync` for short jobs where waiting is acceptable.
- Use `/run` plus `/status/{job_id}` for long jobs.
- Use `/stream/{job_id}` only when the handler yields streaming output.
- Use `/cancel/{job_id}` for abandoned long jobs.
- Use `/health` before blaming the client. It is usually less embarrassing.

### Manage live resources

1. Confirm the exact target by ID/name before changing anything.
2. Prefer read/list/get commands before mutation:

```bash
runpodctl doctor
runpodctl gpu list
runpodctl pod list
runpodctl serverless list
runpodctl template list
runpodctl network-volume list
```

3. For current REST resource management, prefer API v2 at `https://api.runpod.io/v2/...` with `Authorization: Bearer $RUNPOD_API_KEY`; read `references/api-v2.md` first because v2 is beta.
4. Use `https://rest.runpod.io/v1/...` only when the task specifically targets the API v1 surface documented in `references/pods-cli-api.md`.
5. For destructive actions, state the target and impact, then proceed only if the user requested that class of action in this turn.

## Docs Helper

Use the bundled helper to search and fetch official docs without loading the entire site into context:

```bash
python /Users/vavo/.codex/skills/runpod/scripts/runpod_docs.py search serverless handler
python /Users/vavo/.codex/skills/runpod/scripts/runpod_docs.py page serverless/workers/handler-functions
python /Users/vavo/.codex/skills/runpod/scripts/runpod_docs.py openapi --output /tmp/runpod-openapi.json
```

The docs index is `https://docs.runpod.io/llms.txt`. Treat it as the routing table for the docs.

## Output Style

- For implementation tasks, make the code/config changes, run the relevant local checks, and report the exact verification.
- For live infrastructure tasks, include the exact resource IDs touched and the commands/API operations used, with secrets redacted.
- For planning tasks, separate local code changes from Runpod console/API changes.
- For troubleshooting, report observed facts first: command output, endpoint status, logs, response bodies, image tags, and resource IDs. Then give the smallest next action.
