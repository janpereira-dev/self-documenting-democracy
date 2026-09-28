# Compatibility

Install with the existing [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add janpereira-dev/self-documenting-democracy
```

Select `self-documenting-democracy-en`, `self-documenting-democracy-es`, or both.
Requires Node.js/npm and Git, not Python. Private repositories require authorized
GitHub access. Default scope is the current project. `--yes` skips overwrite prompts;
`--copy` uses copies instead of links. No custom installer or global configuration.

Codex uses `$<skill-name>`; Claude Code uses `/<skill-name>`. Skill-specific output
language is explicit, and default output directories are `docs/super-earth/en/`
and `docs/super-earth/es/`. Each installed folder includes every required reference.
Installed bundles contain no Python helpers or other executable scripts.

## Optional native agents — not installed by Skills CLI

| Source | Optional manual destination | Restriction |
|---|---|---|
| `adapters/codex/democracy_archivist.toml` | `.codex/agents/democracy_archivist.toml` | `read-only` sandbox |
| `adapters/claude/democracy-archivist.md` | `.claude/agents/democracy-archivist.md` | `Read, Grep, Glob` only |

The parent selects ONE edition and passes its absolute SKILL.md path. These agents
return drafts, evidence and a resume point; the parent writes documentation.
They do not preload both languages or require the other edition. Native-agent
registration is optional and must be checked in the actual client after setup.
Preserve existing agent definitions; no automatic configuration migration is attempted.

## Safety boundary

The ordinary skill does not establish a filesystem sandbox. Native restrictions
are separate. Read permissions remain host-controlled; a filesystem sandbox does
not turn remote connectors into read-only tools. Never use mutating connectors,
access secrets or send private code out during reconnaissance.

Skills CLI's authorized installation links are not the same as project links
encountered during analysis; do not traverse the latter out of authorized scope.

## Official references

Verified during this project's setup on 2026-09-28:

- [Skills CLI](https://github.com/vercel-labs/skills)
- [Codex agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Claude Code agents](https://code.claude.com/docs/en/sub-agents)

File installation is not marketplace publication, client execution or universal
compatibility with hosted agents and Cowork.
