# Runpodctl Reference

Use this for `runpodctl` command usage, CLI installation/configuration, command groups, output handling, shell completion, file transfer, legacy command migration, and source-repo/package debugging.

## Contents

- Scope
- Official Sources
- Install and Configure
- Command Usage
- Command Groups
- Output and Help
- File Transfer
- Source Repos
- Guardrails

## Scope

Keep `runpodctl` guidance centered on commands the user can run. Prefer the current CLI docs and `runpodctl <command> --help` over REST/GraphQL details. Only drop into REST, GraphQL, or MCP when the CLI cannot express the operation, the user asks for API automation, or existing project code already uses those layers.

## Official Sources

- CLI overview and command reference: `https://docs.runpod.io/runpodctl/overview`
- Source repo: `https://github.com/runpod/runpodctl`
- Homebrew tap: `https://github.com/runpod/homebrew-runpodctl`

Use the docs for current command syntax. Use the source repo for implementation details, release notes, issues, legacy-command behavior, output-format behavior, and debugging the CLI itself. Use the Homebrew tap only for formula/package-manager issues.

## Install and Configure

Common install paths:

```bash
bash <(curl -sL cli.runpod.io)
bash <(wget -qO- cli.runpod.io)
brew install runpod/runpodctl/runpodctl
conda install conda-forge::runpodctl
mamba install conda-forge::runpodctl
pixi global install runpodctl
```

Configure and verify:

```bash
runpodctl doctor
runpodctl config --apiKey YOUR_API_KEY
runpodctl version
```

Every Runpod Pod includes `runpodctl` and a Pod-scoped API key. For local machines, use `runpodctl doctor` for first-time API key and SSH setup. Do not paste real API keys into commands shown back to the user.

## Command Usage

Start with read/list/get commands before mutation:

```bash
runpodctl doctor
runpodctl gpu list
runpodctl datacenter list
runpodctl template search pytorch
runpodctl pod list
runpodctl pod get <pod-id>
runpodctl serverless list
runpodctl network-volume list
```

Common Pod lifecycle commands:

```bash
runpodctl pod create --template-id runpod-torch-v21 --gpu-id "NVIDIA RTX 4090"
runpodctl pod start <pod-id>
runpodctl pod stop <pod-id>
runpodctl pod delete <pod-id>
```

Confirm exact IDs before mutation. Names are useful for humans; IDs keep scripts from doing expensive comedy.

## Command Groups

Current docs organize commands by resource:

- `runpodctl pod ...`: Pods.
- `runpodctl serverless ...` or `runpodctl sls ...`: Serverless endpoints.
- `runpodctl template ...` or `runpodctl tpl ...`: templates.
- `runpodctl hub ...`: Runpod Hub browsing/deployment.
- `runpodctl network-volume ...` or `runpodctl nv ...`: network volumes.
- `runpodctl registry ...` or `runpodctl reg ...`: container registry auths.
- `runpodctl gpu ...`: GPU listing.
- `runpodctl datacenter ...` or `runpodctl dc ...`: datacenters.
- `runpodctl billing ...`: billing history.
- `runpodctl user ...` or `runpodctl me ...`: account info.
- `runpodctl ssh ...`: SSH keys and connection info.
- `runpodctl send` / `runpodctl receive`: file transfer.
- `runpodctl update`, `runpodctl version`, `runpodctl completion`: CLI maintenance.

Check `runpodctl help` and `runpodctl <command> --help` before relying on flags.

## Output and Help

The `runpod/runpodctl` repo documents default JSON output optimized for agents, with `--output` alternatives such as table or YAML:

```bash
runpodctl pod list
runpodctl pod list --output=table
runpodctl pod list --output=yaml
```

Use JSON for automation, table for user-facing terminal summaries, and YAML only when it fits the surrounding workflow.

Enable shell completion:

```bash
runpodctl completion
```

The docs describe completion as idempotent and auto-detecting the shell config file.

## File Transfer

`runpodctl send` and `runpodctl receive` transfer files by connection code and do not require an API key:

```bash
runpodctl send ./data.txt
runpodctl receive <code-from-sender>
```

Use this for ad hoc transfer, not as a durable artifact pipeline. For production workflows, prefer network volumes, object storage, or application-managed storage.

## Source Repos

`https://github.com/runpod/runpodctl` is the Go CLI source repo. It includes command implementation under `cmd/`, API/client logic, release config, docs, and legacy-command notes. The repo is GPL-3.0 licensed.

`https://github.com/runpod/homebrew-runpodctl` is the Homebrew tap. Use it when Homebrew install/update behavior is the problem, not for normal command syntax.

The source README documents legacy command forms such as `get pod`, `create pod`, `remove pod`, `start pod`, and `stop pod` as deprecated. Prefer the noun-first form:

```bash
runpodctl pod get <pod-id>
runpodctl pod create ...
runpodctl pod delete <pod-id>
runpodctl pod start <pod-id>
runpodctl pod stop <pod-id>
```

## Guardrails

- Do not run mutating CLI commands unless the user asked for live resource changes.
- Redact API keys and avoid writing secrets into shell history examples.
- For scripts, use current noun-first commands and JSON output unless the repo already expects another format.
- For CLI bugs, capture `runpodctl version`, command, redacted output, OS/arch, and whether install came from script, Homebrew, direct binary, conda, mamba, or pixi.
