# Runpod Flash Reference

Use this for Runpod Flash SDK/CLI work: `runpod_flash`, `Endpoint`, `GpuType`, `GpuGroup`, `CpuInstanceType`, `NetworkVolume`, `flash dev`, `flash deploy`, and Flash apps.

## Contents

- When To Use Flash
- Setup
- CLI Workflow
- Endpoint Patterns
- Configuration Notes
- Storage
- Troubleshooting
- Further Reading

## When To Use Flash

Use Flash when the user wants to define hardware, dependencies, and remote execution from local Python code instead of writing a raw Serverless handler, Dockerfile, template, and endpoint config by hand. Flash provisions Runpod Serverless workers and routes calls from local code to remote GPU/CPU execution.

Use raw Serverless instead when the project already has a custom worker image, a hand-written handler lifecycle, tight Docker control, non-Python runtime needs, or production infra that should not be hidden behind Flash abstractions.

Flash moves quickly. Refresh official docs before giving exact version support, parameter defaults, or CLI flags.

## Setup

Install:

```bash
pip install runpod-flash
# or
uv add runpod-flash
```

Authenticate:

```bash
flash login
# or, if installed in a uv project:
uv run flash login
```

Flash can also read `RUNPOD_API_KEY` from the environment or a project `.env`. Keep API keys out of committed files. Prefer environment variables for shared projects.

Verify the current Python support in docs before prescribing a version. Recent docs describe macOS/Linux support, Windows through WSL or in-progress Windows support, and Python 3.10+ variants depending on the page/version. Pin `python_version` or use `--python-version` for team consistency.

## CLI Workflow

Common commands:

```bash
flash init PROJECT_NAME
flash login
flash dev
flash build
flash build --exclude scipy,pandas
flash deploy
flash deploy --env staging
flash deploy --app my-app --env production
flash deploy --preview
flash env list
flash env get staging
flash undeploy list
flash undeploy ENDPOINT_NAME
flash undeploy --all
flash update
```

If Flash was installed through uv, prefix commands with `uv run`.

Use `flash dev` for local development with live Runpod workers. Use `flash deploy` for production deployment. After deployment, running the Python script calls the deployed endpoints through Flash resolution. Use `flash deploy --preview` to build and launch a Docker-based local preview instead of deploying to Runpod.

Flash resolves app/environment from configuration, CLI flags, and env vars such as `FLASH_APP` and `FLASH_ENV`; verify exact precedence in current docs. `flash deploy --app ... --env ...` is the explicit path when multiple apps/environments exist.

Deployment artifacts are subject to Runpod Serverless size limits. Current docs describe a 1.5GB deployment limit and auto-exclusion of common base-image packages. Use `flash build --exclude ...`, `flash deploy --exclude ...`, or `--no-deps` when artifacts are too large.

## Endpoint Patterns

Queue-based remote function:

```python
from runpod_flash import Endpoint, GpuGroup

@Endpoint(name="image-worker", gpu=GpuGroup.ANY, workers=(0, 5), dependencies=["torch"])
async def process_image(payload: dict) -> dict:
    import torch
    return {"cuda": torch.cuda.is_available(), "input": payload}
```

Load-balanced HTTP API:

```python
from runpod_flash import Endpoint, GpuGroup

api = Endpoint(name="inference-api", gpu=GpuGroup.ANY, workers=(1, 5), dependencies=["torch"])

@api.post("/predict")
async def predict(payload: dict) -> dict:
    import torch
    return {"ok": True}

@api.get("/health")
async def health() -> dict:
    return {"status": "ok"}
```

Existing endpoint client:

```python
from runpod_flash import Endpoint

endpoint = Endpoint(id="endpoint_id")
job = await endpoint.run({"prompt": "hello"})
await job.wait()
print(job.output)
```

Client-mode jobs support status, waiting, output/error access, and cancellation:

```python
job = await endpoint.run({"prompt": "hello"})
status = await job.status()
await job.wait(timeout=60)
print(job.id, job.output, job.error, job.done)
await job.cancel()
```

Custom Docker image client:

```python
from runpod_flash import Endpoint, GpuType

server = Endpoint(
    name="vllm-server",
    image="vllm/vllm-openai:latest",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
)

models = await server.get("/v1/models")
```

Use `@Endpoint(...)` as a decorator for queue-based Python functions. Use an `Endpoint(...)` instance with route decorators for load-balanced REST APIs. Use `image=` for prebuilt Docker images. Use `id=` to connect to an existing deployed endpoint without provisioning a new one.

## Configuration Notes

- `gpu=` and `cpu=` are mutually exclusive.
- Multiple GPU types can improve availability; use current docs for `GpuType` and `GpuGroup` names.
- `workers=N` means scale from zero to `N`; `workers=(min, max)` controls warm workers and max scale.
- `workers=(1, N)` keeps at least one worker warm and has cost impact.
- Decorated functions and client methods are async in normal use; do not forget `await`.
- Import remote dependencies inside the decorated function or route handler so imports happen on the worker.
- List Python packages in `dependencies=[...]`; list apt packages in `system_dependencies=[...]`.
- Environment variables are passed with `env={...}`; avoid hardcoding secrets in source.
- Check current parameter docs for `idle_timeout`, `max_concurrency`, `execution_timeout_ms`, `min_cuda_version`, `python_version`, `template`, `flashboot`, and `gpu_count`.
- All resources in a Flash app may need compatible Python versions because the app ships as one artifact; pin explicitly when team machines differ.

## Storage

Container disk is temporary worker-local storage. Files not written to the network volume path are erased when the worker stops.

Network volumes mount at `/runpod-volume/` in Flash workers. Use `NetworkVolume(...)` with `volume=` for persistent model caches, datasets, or outputs that must survive worker restarts.

For multi-datacenter endpoints, use one volume per datacenter and do not assume automatic data replication. Flash can find/create volumes by name or reference an existing volume by ID; verify current behavior before writing automation that creates storage.

## Troubleshooting

- Auth error: run `flash login`, set `RUNPOD_API_KEY`, or check `.env` loading.
- Import error on worker: move imports into the `@Endpoint` function/route and add packages to `dependencies`.
- Job stuck in queue: GPU unavailable; use `GpuGroup.ANY`, multiple GPU types, or a different datacenter.
- Template or endpoint name conflict: endpoint names must be unique within the relevant app/environment; undeploy the old endpoint or choose a new name.
- Unexpected cold starts: inspect image/dependency size, `workers` min value, network volume/model loading, and Python version overhead.
- Large payloads: pass object-storage URLs or network-volume paths rather than big inline inputs.

## Further Reading

Prefer official Flash docs for normal usage, especially CLI flags, endpoint parameters, and deployment behavior. Use `https://github.com/runpod/flash` only when debugging the SDK package itself or checking release/source behavior. Use `https://github.com/runpod/flash-examples` when the docs are too thin and a working example is more useful than another theory paragraph.
