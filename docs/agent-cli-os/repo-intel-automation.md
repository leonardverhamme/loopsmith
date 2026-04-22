# Repo Intel Automation

Use this when deciding how repo-intel should stay present and fresh across trusted repos.

## Triggers

There are three automation triggers.

### Repo Entry

When an agent starts in a repo:

- run `agentcli repo-intel status`
- if state is `missing`, `stale_code`, `stale_semantic`, `stale_config`, or `broken`, surface that immediately
- use `agentcli repo-intel ensure` as the repair path

### Scheduled Workspace Audit

Use:

```powershell
agentcli repo-intel audit --all-trusted
agentcli repo-intel audit --all-trusted --fix
```

The audit reads trusted repos from the user config and updates the machine-level workspace registry.

That registry should only contain trusted repos. Temp repos, test fixtures, and untrusted folders must be pruned out during normal audit or status sync.

### Optional Repo-Local Hooks

Hooks and watch mode are opt-in only.

They are useful for very active repos, but they are not the default contract because Graphify's installer and hook ownership model is more invasive than Agent CLI OS should assume for every repo.

## Fix vs Report

Use `--fix` only for safe cases:

- `missing`
- `stale_code`
- `stale_semantic`
- `stale_config`

Treat `broken` as an operator-attention state even though `ensure` can still be the first repair attempt.

When `ensure` repairs `stale_config`, it should also normalize the managed `.gitignore` block so logs, test output, and local agent artifacts stop polluting commits by default.

## Update Policy

Recommended default policy:

- active repos: optional hook or watch setup
- normal repos: `ensure` on entry plus scheduled trusted-repo audit
- note vaults and non-code corpora: less frequent semantic refresh

Recommended git/worktree posture:

- for solo/local work, keep the current local branch as canonical
- treat Codex-managed worktrees as temporary isolation, not as the default place to keep and push durable work
- if a worktree task should survive, hand it off or continue from the local checkout so local commits and pushes do not require merging a worktree branch back
- only create a separate branch when a PR flow or parallel-agent workflow truly needs branch isolation

The important repo-hygiene side effect is intentional:

- trusted repos should pick up the managed `.gitignore` block automatically through `agentcli repo-intel ensure`
- scheduled trusted-repo audits should keep that block from drifting

## CI And Scheduled Validation

Repo-intel does not need its own CI workflow. The normal Python discovery-based test jobs already cover repo-intel code and maintenance regressions.

The important automation boundary is operational freshness, not pipeline duplication:

- CI proves the command contract and state machine still work
- repo entry checks keep the current repo usable
- scheduled audits keep the trusted workspace registry accurate

## Trusted Repo Registry

Trusted repos come from `$CODEX_HOME/config.toml` under `[projects]` with `trust_level = "trusted"`.

Repo-intel does not crawl arbitrary folders by default.
