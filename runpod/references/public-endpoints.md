# Runpod Public Endpoints Reference

Use this for Runpod Public Endpoints: hosted model APIs, model-specific request parameters, image/video/audio/text generation endpoints, Hub playground examples, Vercel AI SDK integration, and model output handling.

## Contents

- When To Use Public Endpoints
- Model Reference
- Request Patterns
- Outputs and Retention
- Cost and Failure Handling
- Integration Notes
- Troubleshooting

## When To Use Public Endpoints

Use Public Endpoints when the user wants to call pre-deployed Runpod-hosted models without deploying their own worker, template, image, or endpoint. Public Endpoints use the same endpoint host shape as queue-based Serverless:

```text
https://api.runpod.ai/v2/{public_endpoint_id}/runsync
https://api.runpod.ai/v2/{public_endpoint_id}/run
https://api.runpod.ai/v2/{public_endpoint_id}/status/{job_id}
```

Use custom Serverless or Flash instead when the user needs custom model weights, custom code, private assets, custom Docker images, or controlled worker lifecycle.

## Model Reference

The model catalog starts at:

```text
https://docs.runpod.io/public-endpoints/models/
```

The root model URL currently redirects to a model page; use the left navigation or `llms.txt` to find the exact model page. Do not hardcode a static model list into the skill because the catalog changes frequently. Current categories include image, video, text, and audio models.

Fetch current model pages before giving exact endpoint IDs, parameter names, allowed ranges, prices, or output schemas:

```bash
python /Users/vavo/.codex/skills/runpod/scripts/runpod_docs.py search public endpoints models
python /Users/vavo/.codex/skills/runpod/scripts/runpod_docs.py search flux dev
```

## Request Patterns

All model inputs go under the `input` object. Model pages define the exact schema.

Synchronous request:

```bash
curl -X POST "https://api.runpod.ai/v2/$MODEL_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input":{"prompt":"A serene mountain landscape","width":1024,"height":1024}}'
```

Asynchronous request:

```bash
curl -X POST "https://api.runpod.ai/v2/$MODEL_ENDPOINT_ID/run" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input":{"prompt":"A futuristic cityscape","width":1024,"height":1024}}'
```

Then poll:

```bash
curl -H "Authorization: Bearer $RUNPOD_API_KEY" \
  "https://api.runpod.ai/v2/$MODEL_ENDPOINT_ID/status/$JOB_ID"
```

Use `/runsync` for quick generations and `/run` for longer jobs, batches, or user-facing workflows that should not block a request thread.

## Outputs and Retention

Model outputs often include URLs, cost fields, delay time, execution time, status, and worker ID. Check the specific model page for exact structure.

Public Endpoint image docs currently state generated image URLs expire after 7 days. Older support KB notes may mention different TTLs for other endpoint families. Treat the model page as authoritative for that model, and tell production apps to copy generated outputs to owned storage if retention matters.

## Cost and Failure Handling

Public Endpoints are usage-based and model-specific. Model pages include price rules such as per-megapixel image pricing or token pricing. Pricing and availability can change; refresh docs before quoting numbers.

Runpod docs state failed generations are not charged for Public Endpoints. Still handle failures explicitly: check `status`, inspect error payloads, preserve job IDs, and avoid retry storms.

## Integration Notes

- Use the Hub playground to test models, tune parameters, estimate cost, and generate starter API code.
- JavaScript/TypeScript projects can use the Runpod Vercel AI SDK provider for supported text, streaming, and image workflows.
- Keep API keys server-side; do not expose `RUNPOD_API_KEY` in browsers or public static apps.
- For model chaining such as text-to-image-to-video, persist intermediate URLs/artifacts before they expire.

## Troubleshooting

- `401` or auth failures: verify API key and header shape.
- `400` validation errors: fetch the current model page and match `input` schema exactly.
- Long wait: switch from `/runsync` to `/run` plus polling.
- Missing output later: generated URL likely expired or was never copied to durable storage.
- Unexpected cost: recompute from the model page pricing and actual output dimensions/tokens/duration.
