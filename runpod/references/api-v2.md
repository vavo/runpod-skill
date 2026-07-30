# Runpod REST API v2 Reference

Use this for current REST resource management. API v2 is currently in beta; refresh the official docs before relying on exact fields or behavior.

## Official sources

- Overview: `https://docs.runpod.io/api-reference-v2/overview`
- Documentation index: `https://docs.runpod.io/llms.txt`
- OpenAPI schema: `https://api.runpod.io/v2/openapi.json`

## Base URL and authentication

The API v2 base URL is:

```text
https://api.runpod.io/v2
```

Send the API key as a bearer token:

```bash
curl --request GET \
  --url "https://api.runpod.io/v2/pods" \
  --header "Authorization: Bearer $RUNPOD_API_KEY"
```

Do not put API keys in URLs, source files, committed config, or shell examples.

## Resource groups

API v2 currently documents Pods, Serverless endpoints, Templates, Network Volumes, Container Registry credentials, Catalog resources, and billing history.

Prefer the generated OpenAPI schema and the linked operation pages for request and response details. Resource paths and fields are beta surface area and may change before general availability.

## Safe workflow

1. Identify the exact resource and ID.
2. Read or list the resource before mutating it.
3. Confirm the requested mutation and its impact.
4. Use the smallest request body that expresses the change.
5. Record the operation and returned status, with secrets redacted.

For Pod state transitions, use the documented action endpoint rather than assuming the API v1 start/stop routes apply to v2.
