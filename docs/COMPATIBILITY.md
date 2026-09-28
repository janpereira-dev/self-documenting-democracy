# Compatibilidad — dos adaptadores, una doctrina

HELLDOCS distribuye una skill compartida y dos agentes nativos. No es un binario
autónomo ni un agente alojado. No requiere API keys propias.

| Entorno | Skill en el proyecto | Agente en el proyecto | Restricción |
|---|---|---|---|
| Codex | `.agents/skills/helldocs/SKILL.md` | `.codex/agents/helldocs_archivist.toml` | `sandbox_mode = "read-only"` |
| Claude Code | `.claude/skills/helldocs/SKILL.md` | `.claude/agents/helldocs-archivist.md` | Solo `Read, Grep, Glob` |

El instalador copia desde `skills/helldocs/` y `adapters/`. No duplica manualmente
la doctrina por plataforma. Los adaptadores contienen diferencias de permisos,
carga e invocación. Cada entorno hereda su modelo configurado.

Claude tiene la skill precargada y construye inventario con herramientas de lectura;
no ejecuta el helper Python. El orquestador puede ejecutarlo si su host lo permite.
En ambos casos, el subagente retorna contenido y el orquestador escribe únicamente
la documentación autorizada.

## Instalación por proyecto

Desde el clon: `python install.py <project-path> --platform both --apply`.
Sin `--apply`, solo muestra destinos. `codex` es el valor predeterminado.
Los conflictos se detectan en todos los destinos antes de empezar a copiar.
No se prometen transacciones frente a fallos de disco o cambios concurrentes.

No modifica `AGENTS.md`, `CLAUDE.md`, hooks, configuración global ni marketplaces.
Para actualizar, revise y fusione cambios con sus archivos existentes: el instalador
deliberadamente no tiene modo de sobrescritura forzada.

## Distribución futura

Publicar el repositorio no equivale a publicarlo como plugin ni subir la skill a
Claude.ai. No se promete compatibilidad con Cowork, agentes alojados ni todos los
proveedores a partir de este adaptador local. Manifiestos de marketplace, aprobación
y pruebas de cada host son etapas distintas y siguen pendientes.

## Límites de seguridad

El allowlist de Claude restringe herramientas; no redefine los directorios que el
host permite leer. El sandbox de Codex restringe archivos, pero no convierte todos
los conectores MCP en herramientas de solo lectura. Las instrucciones prohíben
herramientas mutantes y acceso a secretos, además de las restricciones del host.

La skill usada directamente por el agente principal permite escritura documental:
no impone técnicamente una allowlist de extensiones o directorios. Verifique el diff.
El inventario usa nombres de archivo para exclusiones conservadoras; no es un
escáner completo de secretos ni una protección frente a cambios concurrentes maliciosos.

## Fuentes oficiales consultadas el 2026-09-28

- [Codex: agentes](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex: skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: subagentes](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: skills](https://code.claude.com/docs/en/skills)

Formatos contrastados con documentación; carga y ejecución real aún no verificadas.
