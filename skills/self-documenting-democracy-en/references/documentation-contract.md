# Field report contract

## Default output

Use `docs/super-earth/en/`; never overwrite the Spanish edition's directory.

- `README.md`: Spokesperson opening, actual purpose, scope, snapshot and index.
- `architecture.md`: system map, boundaries, evidenced decisions and dependencies.
- `modules/`: reports for meaningful modules, not one page per trivial file.
- `flows.md`: main paths, failures, synchrony and side effects.
- `data.md`, `interfaces.md`, `integrations.md`: only for existing fronts.
- `operations.md`: startup, variable names, declared CI/CD, existing tests,
  documented but unexecuted commands, observability and recovery.
- `unknowns.md`: contradictions, inferences, supported risks and pending work.
- `coverage.json`: inventory plus reading and documentation state.
- `evidence.md`: navigable technical source register.
- `assets/`: copied insignia actually used.

Combine chapters for small projects; retain index, evidence and coverage.
Do not create empty chapters just to satisfy this list.

## Module report

1. Spokesperson: short fictional opening.
2. Mission: responsibility and boundaries, using actual names.
3. Coordinates: paths and symbols.
4. Inputs/outputs: types, contracts, validation, failures.
5. Maneuver: verified flow and dependencies.
6. Risks and limits: facts, inferences and open questions separately.
7. Tests: existing files and cases; explicitly state when not executed.
8. Samples: source and evidence links.
9. Next order: recommended reading or verification, not automatic repairs.

## Evidence

Use IDs such as `E-001`. Important claims link to a record containing a relative
path, inspected symbol or line range, snapshot and explanation. File links are
relative to the document. Include line ranges in text as well as optional fragments
such as `#L10-L20`. Never invent a path to make a claim appear substantiated.

Claim states: `observed`, `inferred`, `unknown`, `contradicted`. Comments and READMEs
can be stale: report conflicts with implementation rather than silently choosing
one. Static observations do not establish production behavior.

## Honest coverage

The optional helper emits `entries` with `path`, `kind`, `status`, `reason` and
metadata. Preserve these and add `read_ranges`, `evidence_ids`, `document`,
`documented`. Manual inventories follow the same contract.
File states: `pending`, `read`, `partial`, `excluded`, `blocked`.
A pruned directory is ONE directory entry; its interior file count is unknown.
Do not count it as a read file or hide it from the report.

Report candidate files; complete/partial/pending/blocked reads; excluded files and
directories with reasons; documented and non-applicable modules; inventory errors
and out-of-scope paths. If reporting a percentage, use
`read / (read + partial + pending + blocked)` for candidate FILES with an explicit
denominator. Zero denominator means `not_applicable`, never 100%.
Reading and documenting are separate dimensions. Exclusions, errors or partial
reads prohibit claiming that the entire project has been read.

## Continuation

Checkpoint large projects inside the documentation destination: snapshot, completed
sectors, pending queue, next file/range. Mark affected evidence stale when sources
change and reread before reuse. Prior docs do not replace inspecting a new revision.

## Protection limits

The skill defines a behavioral documentation-only contract, NOT a write sandbox.
Optional native adapters return drafts under their own restrictions; the parent
checks the destination before writing. A filesystem sandbox does not automatically
make remote MCP connectors read-only. Never invoke mutating connectors for this task.
