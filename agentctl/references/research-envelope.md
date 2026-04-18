# agentctl Research Envelope

`agentctl research web|github|scout` writes two artifacts:

- `evidence.json`
- `brief.md`

Shared evidence fields:

- `schema_version`
- `track`
- `query`
- `generated_at`
- `provider`
- `sources`
- `shortlist`
- `caveats`
- `final_recommendation`

Use this contract when a research skill needs:

- a machine-readable artifact for later automation
- a compact human-readable brief
- one stable format across web, GitHub, and hybrid scouting

Preferred commands:

```text
python ../agentctl.py research web "<query>"
python ../agentctl.py research github "<query>"
python ../agentctl.py research scout "<query>"
```
