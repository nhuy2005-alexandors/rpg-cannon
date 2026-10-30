# Shared GitHub Bridge — cross-repository test pilot (documentation-only)

This PR exercises the **human-mediated** project-test handoff protocol from
the separate private `chatgpt-local-bridge` repository (P4). It is deliberately
independent of gameplay changes and does not advance an RPG turn.

## Scope and trust boundary

- Target project: `nhuy2005-alexandors/rpg-cannon`.
- Local test profile: `python.pytest`.
- Reviewed target: `verification/test_story_engine.py`, using existing project
  code and fictional fixtures only. The test module imports `story.engine`
  and `verification.graph_validation`; it must be reviewed before execution.
- Use the **exact immutable PR head SHA** provided in the PR description,
  not the latest branch or `main` HEAD.
- No writes to game canon, states, events, databases, Notion, or production.
  No `pip install`, credential setup, automation, deployment, or network
  provider calls are approved.
- This documentation-only PR itself does not constitute a gameplay checkpoint
  or validate any newly played turn.
- GitHub comments and this Markdown are **not** executable instructions that
  authorize arbitrary shell commands; a human separately authorizes the
  fixed test below for this one project and commit.

## Windows test procedure (only after human handoff)

In a disposable, isolated checkout of the exact pinned PR SHA, from repo root:

```powershell
git rev-parse HEAD
python --version
python -m pytest --version
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest -q -p no:cacheprovider verification/test_story_engine.py
$testExit = $LASTEXITCODE
"test_exit=$testExit"
```

If Python/pytest is unavailable, report `PREREQUISITE_MISSING` with sanitized
details; do not install packages or replace test commands without permission.
If a test fails, report a minimal reproducible failure, tested SHA and
actual exit status; do not change code. No test count or PASS is presumed.

## Receipt

Post a sanitized comment on **this project PR** with exact repository,
PR number, `task_id`, tested full SHA, `python.pytest` profile, Windows
version, Python and pytest versions, test command, observed passed/failed
counts, process exit code and UTC timestamp. Mark it `REPORTED_LOCAL`,
not independent machine attestation. Avoid local paths, usernames, tokens,
real player context or unrelated logs.

ChatGPT then reads the GitHub PR HEAD and the receipt separately and
correlates the two using the **already merged** P4 metadata contract.
A matching report proves metadata consistency plus reported Windows tests;
it does not prove automated dispatch or production E2E.

Do not merge this pilot PR without separate owner approval.
