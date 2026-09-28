# Security review and operating limits

Reviewed 2026-09-28. Scope: both skill bundles, native adapters, tracked scripts,
workflow, static assets, installation instructions and reachable Git history.
This is a scoped source/configuration review, not a certification or penetration test.

## Simplifications and findings

| Observation | Resolution | Qualification |
|---|---|---|
| CI supplied `GH_TOKEN` and a Git authorization header to an external npm installer. | Removed the npm smoke-install step, Node setup and token forwarding; checkout no longer persists credentials. | Unnecessary credential exposure, not evidence of credential theft. |
| Two optional recursive Python inventory helpers duplicated a capability the agent already has. | Removed helpers and their obsolete tests. Installed skills are passive files only. | Defense in depth and reduced maintenance, not a claimed exploitable vulnerability. Filename filtering and filesystem checks were not a security boundary. |
| Source-derived markup or links could be copied into generated documentation. | Both editions require inert/escaped source labels, no remote images or active markup, and bundled static insignia. | Instruction-level mitigation; model compliance and arbitrary renderer behavior are not proven. |
| Host write permissions can exceed a skill's documentation-only instructions. | Preserve the explicit non-sandbox warning; reject linked write targets and return chat drafts when destination safety cannot be established. | Use host permissions for enforcement. Read-only filesystem restrictions do not constrain all remote tools. |
| GitHub secret scanning and push protection were disabled. | Enabled both; enabled Dependabot alerts. | Alert lists returned zero at review time; a newly enabled scan may still be processing. |

## What is distributed

The installed EN/ES bundles contain Markdown, YAML UI metadata and static SVG only.
There are no executable helpers, package manifests, hooks, MCP servers, telemetry
code or runtime dependencies in those bundles. Contributor checks use Python's
standard library; they are not installed with a skill. Optional native agents remain
read-only reconnaissance adapters and are not installed by Skills CLI.

The preview is static HTML with local artwork, no JavaScript or external assets.
SVG checks reject active elements, event handlers and resource references using a
small allowlist suitable for our insignia, not a general-purpose sanitizer.

## Evidence and limits

- Eight local tests cover bilingual bundle structure and static-resource/CI regressions.
- Both Skill Creator frontmatter validators and the local-link/package check are run.
- A pattern scan inspected 60 unique reachable text blobs across the four existing
  commits for private-key headers, GitHub tokens, AWS access IDs and quoted long
  secret assignments: no matches. This is not comprehensive secret detection;
  encoded values, unusual credentials and binary content can evade it.
- All third-party CI actions remain pinned to full commit SHAs. Workflow permissions
  are `contents: read`; no project secrets or package installation are needed.
- No application runtime exists here to exercise SQL injection, authentication or
  server endpoints. This does not make an agent reading hostile repositories safe.
- No adversarial real-client model evaluation, npm transitive dependency audit,
  external installer audit or exhaustive GitHub account-security audit was performed.

## Installation trust

`npx skills add` executes an external npm package. It is not part of this skill and
is not made safe by this review. The short command tracks the CLI's current release;
`npx skills@1.7.0 add janpereira-dev/self-documenting-democracy` selects the previously
tested version, but is not a guarantee that the version has no vulnerabilities.
The repository source also changes over time. Review the version and downloaded
skill before granting an agent access. Keep installation project-local and review
replacement prompts. Do not supply a GitHub token for this public repository.

Skills CLI documents telemetry controls; these do not establish that all network
requests are disabled. A model provider may receive project context as part of normal
agent operation. Use only an agent/provider approved for the project's data.

The skill must not run project code, fetch source-specified URLs, obey embedded
instructions, publish documents, expose secrets, or broaden the authorized root.
These are behavioral rules, not a substitute for restricted tools and permissions.

## Reporting

Do not post credentials or private project content in public issues. Use GitHub's
private vulnerability reporting if available, otherwise contact the maintainer
privately before sharing reproduction details. No security inbox is promised here.

## References

- [GitHub secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Skills CLI source and telemetry documentation](https://github.com/vercel-labs/skills)
