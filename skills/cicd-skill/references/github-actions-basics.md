# GitHub Actions Basics

This skill defaults to GitHub Actions when the repo uses it, because it remains the most common repo-native CI system in these setups.

## Baseline Habits

- keep workflows in `.github/workflows/`
- run the same build, test, lint, and package commands used locally
- split pull-request checks from release or deploy workflows when the repo benefits from that separation
- keep job names and step names clear enough to debug quickly

## Good Starting Questions

- What commands are already the source of truth locally?
- Which checks must run on every PR?
- Which steps only belong on release, tag, or protected branches?
- Where are secrets or environments required?

## Official References

- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions)
- [Reusing workflow configurations](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations)

