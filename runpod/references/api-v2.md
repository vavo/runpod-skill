# Runpod REST API v2 Reference

Use this for current REST resource management. Refresh the official docs before relying on exact fields or behavior; v2 is an actively evolving API surface.

## Official sources

- Overview: `https://docs.runpod.io/api-reference-v2/overview`
- Migration guide: `https://docs.runpod.io/api-reference-v2/migrate-from-v1`
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

API v2 currently documents account SSH keys and secrets, Pods, Instant Clusters, Serverless endpoints and builds, Templates, Network Volumes, Container Registry credentials and ECR delegations, catalog resources, public templates, and billing history.

Prefer the generated OpenAPI schema and the linked operation pages for request and response details. Resource paths and fields may change as Runpod evolves the API.

## Safe workflow

1. Identify the exact resource and ID.
2. Read or list the resource before mutating it.
3. Confirm the requested mutation and its impact.
4. Use the smallest request body that expresses the change.
5. Record the operation and returned status, with secrets redacted.

## Important v1 differences

- v1 is deprecated and is scheduled for retirement on November 15, 2026. Migrate existing integrations before that date.
- Resource paths move to the v2 base URL. Examples include `/v2/serverless`, `/v2/network-volumes`, and `/v2/clusters`.
- Pod lifecycle operations use `POST /v2/pods/{id}/action` with `{"action":"start|stop|restart|terminate"}`. The v1 `reset` action has no v2 equivalent.
- List responses are wrapped by resource name, such as `{"pods":[...]}` and `{"networkVolumes":[...]}`, instead of returning a bare array.
- v2 uses nested create/update shapes and RFC 9457-style problem responses with `title`, `status`, and `detail`.

Use the migration guide for field-by-field mappings and the OpenAPI schema for operation details.
