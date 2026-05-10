# Runpod Serverless Reference

Use this for Runpod Serverless workers, endpoints, job requests, Docker packaging, local testing, vLLM, and cold-start work.

## Contents

- Concepts
- Handler Patterns
- Python SDK Client
- Local Testing
- Docker Packaging
- Queue Endpoint Requests
- Endpoint Configuration
- Support KB Notes
- vLLM and OpenAI Compatibility
- Troubleshooting Checklist

## Concepts

- Endpoint: public API target for a Serverless application.
- Worker: container instance that runs the handler or custom HTTP service.
- Queue-based endpoint: uses `/run`, `/runsync`, `/status`, `/stream`, `/cancel`, `/retry`, `/purge-queue`, and `/health`.
- Load-balancing endpoint: routes direct HTTP traffic to custom routes exposed by the worker, usually FastAPI/Flask/vLLM style.
- Cold start: time from request arrival to a ready worker. Image size, model download, volume locality, and initialization all matter.

## Handler Patterns

Minimal Python handler:

```python
import runpod

def handler(job):
    data = job.get("input") or {}
    return {"ok": True, "input": data}

runpod.serverless.start({"handler": handler})
```

Streaming handler:

```python
import runpod

def handler(job):
    for item in ["one", "two", "three"]:
        yield item

runpod.serverless.start({
    "handler": handler,
    "return_aggregate_stream": True,
})
```

Keep model loading and heavyweight clients outside the handler so a warm worker can reuse them. Validate input before GPU work. Return URLs for large outputs instead of forcing big payloads through endpoint responses.

## Python SDK Client

The official Python package is `runpod`.

Install and configure:

```bash
pip install runpod
# or
uv add runpod
```

```python
import os
import runpod

runpod.api_key = os.getenv("RUNPOD_API_KEY")
endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))

request = endpoint.run({"prompt": "hello"})
print(request.status())
print(request.output())

result = endpoint.run_sync({"prompt": "hello"})
print(result)
```

Do not hardcode API keys. The Python SDK supports a global `runpod.api_key`; `runpod.Endpoint(..., api_key="...")` can override it for a specific endpoint. Use separate endpoint instances for concurrent work with different API keys.

For Serverless worker startup validation, `runpod-python` supports fitness checks:

```python
import runpod
import torch

@runpod.serverless.register_fitness_check
def check_gpu():
    if not torch.cuda.is_available():
        raise RuntimeError("GPU not available")

def handler(job):
    return {"ok": True}

runpod.serverless.start({"handler": handler})
```

Use fitness checks for GPU availability, model files, disk space, external service connectivity, and required environment config. A failed fitness check exits the worker before it starts taking jobs, which is better than quietly accepting work it cannot run.

## Local Testing

Common commands:

```bash
python handler.py --test_input '{"input": {"prompt": "hello"}}'
python handler.py --test_input test_input.json
python handler.py --rp_serve_api --rp_log_level DEBUG
python handler.py --rp_serve_api --rp_api_concurrency 4
```

When testing the local API server, send HTTP POST requests from a second terminal. The local `/run` path only returns a fake request ID in current docs; use `/runsync` to execute the handler locally. Use concurrent testing only when the handler is designed for it; otherwise you are measuring chaos, not throughput.

## Docker Packaging

Typical layout:

```text
Dockerfile
requirements.txt
src/handler.py
```

Typical Dockerfile shape:

```dockerfile
FROM python:3.11-slim

WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/handler.py /handler.py

CMD ["python", "-u", "/handler.py"]
```

Use CUDA/framework base images only for GPU workloads that need them. Add `.dockerignore` before building. Prefer cached models or network volumes for large models when the docs and workload fit.

## Queue Endpoint Requests

Base URL:

```text
https://api.runpod.ai/v2/{endpoint_id}
```

Common operations:

```bash
curl --request POST \
  --url "https://api.runpod.ai/v2/$ENDPOINT_ID/runsync" \
  --header "authorization: $RUNPOD_API_KEY" \
  --header "content-type: application/json" \
  --data '{"input":{"prompt":"hello"}}'

curl --request POST \
  --url "https://api.runpod.ai/v2/$ENDPOINT_ID/run" \
  --header "authorization: $RUNPOD_API_KEY" \
  --header "content-type: application/json" \
  --data '{"input":{"prompt":"hello"}}'

curl --request GET \
  --url "https://api.runpod.ai/v2/$ENDPOINT_ID/status/$JOB_ID" \
  --header "authorization: $RUNPOD_API_KEY"
```

Use `/runsync` for short work; use `/run` and polling for long jobs. Check the current docs for payload limits, retention, wait parameters, and rate limits before giving exact numbers.

## Endpoint Configuration

Verify current fields before creating or updating endpoints. Common concerns include:

- `workersMin` and `workersMax`
- GPU type IDs and fallback order
- CPU instance IDs for CPU endpoints
- execution timeout
- idle timeout
- scaler type/value
- network volume IDs
- container image/template ID
- environment variables and secrets

Changes to image, GPU types, env vars, or worker counts can restart workers or alter billing. Say that plainly before doing it.

## Support KB Notes

Runpod also publishes a support/assistant knowledge base. Treat it as secondary support material, not a replacement for official docs/API references. Useful topics include:

- Builds stuck in `PENDING`: check `https://status.runpod.io`, retry after a reasonable wait, and inspect Dockerfile/image size before assuming user error.
- Programmatic Pod logs: the support KB says there is no public REST API or SDK method for Pod logs; use console logs, app-level external logging, or write logs to a network volume.
- Driver/CUDA and Blackwell: verify current driver/CUDA compatibility and image recommendations before advising on RTX 5090/B200/Blackwell issues.
- Temporary image URLs: generated image URLs may expire; production apps should download outputs or move them to owned storage.
- Serverless WebSocket pattern: long-lived bidirectional traffic can use exposed TCP ports and worker-reported `RUNPOD_PUBLIC_IP` / `RUNPOD_TCP_PORT_<port>` details, but this is a specialized pattern that should be checked against current examples before implementation.

## vLLM and OpenAI Compatibility

Use vLLM-specific docs when the request is about LLM serving, OpenAI-compatible APIs, chat/completions routes, tokenizer/model config, tensor parallelism, or environment variables. Do not mix queue-based `/run` assumptions into load-balanced OpenAI-compatible vLLM endpoints unless the docs and endpoint type confirm it.

## Troubleshooting Checklist

1. Confirm endpoint ID, endpoint type, image/template, worker count, and GPU type.
2. Hit `/health` or inspect Runpod console health/logs.
3. Check recent worker logs before changing code.
4. Reproduce locally with `--test_input` when possible.
5. Check image pull errors, missing files, bad `CMD`, dependency install failures, CUDA mismatch, model download failures, storage paths, and payload size.
6. For slow starts, inspect image size, model load path, cache/volume usage, `workersMin`, and GPU availability.
