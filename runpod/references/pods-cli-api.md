# Runpod Pods, CLI, API, and Storage Reference

Use this for Pods, templates, network volumes, REST API work, and Runpod MCP setup. For `runpodctl` command usage and CLI repo details, read `runpodctl.md`.

## Contents

- Tool Preference
- Runpod MCP
- REST API
- Pods
- Templates
- Network Volumes
- Ports and Access
- Cost Guardrails

## Tool Preference

Prefer tools in this order:

1. Runpod MCP server, if configured and the user asked for live resource management.
2. `runpodctl`, if installed and authenticated; read `runpodctl.md` before giving CLI-specific commands.
3. REST API with `RUNPOD_API_KEY`.
4. GraphQL only when the task specifically needs GraphQL or existing project code already uses it.
5. Official docs for planning, review, and dry-run answers.

For live mutations, list/get first. IDs beat names. Names are for humans and bugs.

## Runpod MCP

Runpod documents two MCP servers:

- API MCP server via `npx -y @runpod/mcp-server@latest`, authenticated with `RUNPOD_API_KEY`.
- Docs MCP server for documentation search, no API key required.

The API MCP server source is `https://github.com/runpod/runpod-mcp`. It requires Node.js 18 or newer and exposes infrastructure tools for Pods, Serverless endpoints, templates, network volumes, and container registry auths. The npm package is `@runpod/mcp-server`; the package binary is `runpod-mcp`.

For Codex CLI, the documented API MCP setup shape is:

```bash
codex mcp add runpod --env RUNPOD_API_KEY=your_api_key_here -- npx -y @runpod/mcp-server@latest
```

Do not install or reconfigure MCP servers unless the user asks. If missing, give the command with the token placeholder, not the token.

Treat the API MCP server as a live infrastructure control plane. Its `RUNPOD_API_KEY` can grant broad account access, so prefer a scoped/separate API key when the user's account model supports it, never commit `.mcp.json` with secrets, and list/get resources before mutating them.

If developing or debugging the MCP server itself, use the local-build path from the repo:

```bash
git clone https://github.com/runpod/runpod-mcp.git
cd runpod-mcp
pnpm install
pnpm build
node /absolute/path/to/runpod-mcp/dist/index.mjs
```

The implementation uses REST for authenticated CRUD operations and GraphQL for public read-style infrastructure queries such as GPU types and data centers. Verify current tool names from the installed MCP server before giving exact MCP-tool instructions.

## REST API

Base URL:

```text
https://rest.runpod.io/v1
```

Authentication:

```text
Authorization: Bearer $RUNPOD_API_KEY
```

Core resources:

- `/pods`
- `/endpoints`
- `/templates`
- `/networkvolumes`
- `/containerregistryauth`
- `/billing/...`

Fetch the current OpenAPI spec before generating clients or writing non-trivial automation:

```bash
curl --request GET \
  --url "https://rest.runpod.io/v1/openapi.json" \
  --header "Authorization: Bearer $RUNPOD_API_KEY"
```

## Pods

Use Pods for development, notebooks, training, long-running services, manual debugging, and cases where a stable machine is more useful than autoscaling request handling.

Before creating a Pod, identify:

- GPU type and count
- cloud type / datacenter requirements
- template or image
- container disk size
- volume size or network volume
- ports to expose
- SSH/Jupyter/VS Code access needs
- secrets and env vars
- stop/terminate policy

For troubleshooting, inspect actual Pod state first: GPU visibility, container logs, disk usage, exposed ports, SSH status, and template image.

## Templates

Templates package image, ports, disk/volume sizing, env vars, and startup behavior. Use custom templates when the same deployment shape will be reused. Keep secrets in Runpod secrets or runtime env config, not baked into templates or Docker images.

For Serverless templates, verify whether `isServerless` is required and whether the container command starts the worker correctly.

## Network Volumes

Network volumes provide persistent storage independent of compute. Serverless workers mount attached volumes at `/runpod-volume`. Pods typically mount network volumes at `/workspace`.

Use network volumes for:

- model files shared across workers
- datasets
- generated artifacts that must outlive worker/container lifecycle
- reducing repeated downloads

Constraints to verify in current docs:

- datacenter availability and GPU availability
- whether volume can be attached after resource creation
- multi-volume/multi-region behavior
- S3-compatible access details
- concurrent write risks

Never imply data is replicated across volumes unless the docs or user setup says so.

## Ports and Access

For Pods, distinguish:

- HTTP proxy ports for browser/API access.
- TCP ports for SSH or raw services.
- Private networking/global networking for internal Runpod communication.

For Serverless load-balancing endpoints, distinguish custom route traffic from queue-based `/run` operations.

## Cost Guardrails

Mention cost impact when actions can keep compute or storage running:

- `workersMin > 0`
- On-demand Pods left running
- large network volumes
- oversized container disks
- GPU fallback lists with expensive GPUs
- repeated image pulls/cold starts

Do not turn every answer into a billing sermon. One crisp warning is enough.
