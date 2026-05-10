# Runpod GraphQL Reference

Use this when a task specifically needs Runpod GraphQL schema details, legacy code already uses GraphQL, or the requested data is easier to fetch from GraphQL than REST/runpodctl/MCP.

## Contents

- Spec and Endpoint
- When To Use GraphQL
- Safe Query Patterns
- Mutations
- Drift Guardrails

## Spec and Endpoint

Official interactive spec:

```text
https://graphql-spec.runpod.io
```

Endpoint and auth:

```text
POST https://api.runpod.io/graphql
Authorization: Bearer <RUNPOD_API_KEY>
Content-Type: application/json
```

The spec lists common queries, mutations, and types for Pods and related infrastructure. It currently advertises version `1.1.0`; do not assume that remains current.

## When To Use GraphQL

Prefer GraphQL when:

- Existing project code already uses Runpod GraphQL.
- You need schema-driven fields or nested Pod details not exposed cleanly by REST/runpodctl.
- You need infrastructure availability queries such as `gpuTypes` or `cpuTypes`.
- You are maintaining older automation using mutations like `podRentInterruptable`, `podFindAndDeployOnDemand`, `podStop`, `podResume`, or `podTerminate`.

Prefer MCP, runpodctl, or REST for normal live resource management when those tools cover the task. They are usually clearer and less schema-fragile.

## Safe Query Patterns

Start with read-only queries:

```bash
curl -sS "https://api.runpod.io/graphql" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query gpuTypes { gpuTypes { id displayName memoryInGb secureCloud communityCloud } }"}'
```

Useful spec entries to check before writing code:

- `gpuTypes`
- `cpuTypes`
- `myself`
- `pod`
- `Pod`
- `PodRuntime`
- `PodTemplate`
- `NetworkVolume`
- `ContainerRegistryAuth`

Request only the fields the caller needs. GraphQL examples in generated docs can contain placeholder-looking values; treat field names as useful and example values as disposable.

## Mutations

GraphQL mutations can create, resume, stop, terminate, or edit Pods and related resources. Treat them as live infrastructure mutations:

1. Query the target resource first.
2. Confirm exact IDs and current state.
3. Keep secrets out of query strings and logs.
4. Prefer dry-run/planning text unless the user explicitly asked to mutate resources.
5. Report mutation name, target ID, and returned status with secrets redacted.

Common mutation names in the public spec include:

- `podFindAndDeployOnDemand`
- `podRentInterruptable`
- `podResume`
- `podStop`
- `podTerminate`
- `podEditJob`
- `saveRegistryAuth`

Verify current input types in the spec before writing mutation payloads.

## Drift Guardrails

GraphQL schema changes can break automation silently if code assumes fields. Before making non-trivial changes:

- Open `https://graphql-spec.runpod.io` or search current Runpod docs.
- Compare existing code's queries/mutations against the current spec.
- Keep generated clients/schema snapshots out of the skill unless the user asks for a repo-local implementation.
- Use REST OpenAPI for REST resources and GraphQL spec only for GraphQL resources; do not mix endpoint hosts.
