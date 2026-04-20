# Prompt Template

Use this when you want a repeatable short prompt for normal testing work.

```text
Use $test-skill for this task.

Task:
[describe the feature, bug, or code change]

Requirements:
- Inspect the repo's existing test stack first.
- Choose the right layer instead of defaulting blindly to unit or e2e.
- Prefer repo-native CLIs first and CLI-based browser workflows before MCP.
- Add regression coverage when this is a bug fix.
- Run the smallest correct validation before stopping.
- If a correct test fails, fix the code or setup rather than weakening the test.
- Keep iterating until the relevant suites are green or a real blocker remains.

Output:
- chosen test layer
- added or updated tests
- commands run
- remaining risk
```

