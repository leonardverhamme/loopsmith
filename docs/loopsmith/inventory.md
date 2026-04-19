<!-- loopsmith:auto-generated -->
# Loopsmith Inventory

The raw autodetected inventory is stored at `agentctl/state/inventory.json`.

## Purpose

- Detect what is actually present on the machine and in Codex.
- Keep raw installed surface separate from the curated capability menu.
- Let `capabilities` stay compact while `inventory` remains the debugging and inspection layer.

## Commands

- `loopsmith inventory refresh`
- `loopsmith inventory show --kind all --scope all`
- `loopsmith inventory item <kind>:<name>`

## Item Shape

- `id`
- `kind`
- `name`
- `source_scope`
- `status`
- `installed` or `configured`
- `version` when available
- `source_path` or `source_hint`
- `front_door_candidate`
- `menu_bucket`
- `hidden_reason`

## Menu Budget

- Raw inventory items per bucket: <= 25
- Raw buckets split deterministically when the item budget is exceeded.

## Current Summary

```json
{
  "bucket_count": 8,
  "hidden_count": 14,
  "kind_counts": {
    "plugin": 1,
    "skill": 106,
    "tool": 16
  },
  "max_bucket_size": 25,
  "status": "ok",
  "total_items": 123
}
```

## Detection Sources

- `tools`: `ok`
  - 16 detected tools
- `skills-global`: `ok`
- `skills-project`: `ok`
  - 34 project skills
