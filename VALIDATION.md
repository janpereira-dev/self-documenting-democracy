# Validation record — 2026-09-28

## Current simplified package

- 8/8 local tests pass: five bilingual bundle checks and three security regression
  checks (including six active/external SVG payloads rejected).
- Package validator checks local links, adapter contracts, independently contained
  editions, a static SVG allowlist and two PNG headers.
- Both Skill Creator structural validators pass.
- Installed bundles contain no executable helpers. Python is contributor-only.
- CI runs these repository checks on Windows and Linux with read-only repository
  permissions and no persisted checkout credentials. It no longer executes npm
  or passes a GitHub token to a package installer.

## Historical installation evidence

Before the simplification, commit `980fd2f` passed installation of EN alone, ES
alone and both for Claude Code and Codex with Skills CLI 1.7.0 on Windows and Linux:
[run 36387327674](https://github.com/janpereira-dev/self-documenting-democracy/actions/runs/36387327674).
That result is historical, not a fresh installation test of every later commit.

## Limits

Structural checks are not proof of model adherence, narrative quality, semantic
translation equivalence, runtime client discovery or absence of vulnerabilities.
Real-client acceptance scenarios remain in [maintenance](docs/MAINTENANCE.md).
See [security review](SECURITY.md) for scope, removed risk and residual trust boundaries.
No marketplace approval or complete security guarantee is claimed.
