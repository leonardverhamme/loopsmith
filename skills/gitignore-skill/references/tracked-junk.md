# Tracked Junk Handling

`.gitignore` only affects untracked files. If junk is already committed, tightening `.gitignore` is not enough by itself.

## Recommended Checks

- `git status --short`
- `git ls-files <path>`
- `git check-ignore -v <path>`

Use these to distinguish:

- untracked local noise
- tracked generated junk
- source-of-truth files that only look noisy

## Safe Default

If files are already tracked:

1. add the correct `.gitignore` rule first
2. explain that tracked files will still remain in git
3. only propose or run `git rm --cached` if the user explicitly wants the cleanup or the repo contract is already obvious

## Do Not Untrack By Guesswork

Be especially careful with:

- generated docs that are intentionally committed
- test fixtures and screenshots
- package manager lockfiles
- built assets that are part of deployment
- data snapshots used for regression testing

The presence of generated content does not prove it should be removed from version control.

## Communication Pattern

When tracked junk exists, report it plainly:

- what is still tracked
- which `.gitignore` rule was added or should be added
- whether an explicit untrack step is still needed

Do not hide the tracked-vs-untracked distinction.
