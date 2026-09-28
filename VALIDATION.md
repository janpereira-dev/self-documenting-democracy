# Validation record — 2026-09-28

## Scope

Two independently installable editions: English and Spanish. Checks distinguish
bundle structure, file installation and actual model behavior.

## Local results

14/14 unit tests passed (9 inventory + 5 bilingual packaging). Both Skill Creator
structural validations passed. Package validation checked 33 local links, native
adapter invariants and two PNG headers.

## Automated checks

- Inventory helper regression tests, including sensitive filenames, pruning,
  metadata-only operation, large files, access errors and Unicode paths.
- Bilingual package tests: matching resource sets, byte-identical optional helpers,
  equivalent machine-readable states, source URL parity and separate output paths.
- Package validator: native adapter invariants, both skill identities, local links,
  no cross-bundle runtime dependencies, SVG parsing and PNG headers.
- Skill Creator structural validator is run separately for each edition.
- CI on Linux and Windows installs EN alone, ES alone and both using Skills CLI
  1.7.0, then checks the installed content. Check the actual workflow result;
  this file alone does not establish a successful remote run.

## Limits

These checks do not prove narrative quality, semantic translation equivalence,
real-client discovery, model adherence, or a complete security boundary. The manual
language/safety scenarios in [maintenance](docs/MAINTENANCE.md) still require
real-client behavioral evaluation. No marketplace approval is claimed.

The earlier single-skill installation was verified on Linux and Windows. The new
bilingual distribution must pass its own pipeline; do not transfer that claim.

Python is used for contributor tests and an optional metadata helper only. Users
install with the existing Skills CLI and do not need Python.
