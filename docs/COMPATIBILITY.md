# Instalación estándar: Skills CLI

Desde el proyecto de destino:

```sh
npx skills add janpereira-dev/helldocs
```

Seleccione el entorno en el asistente. Para Claude Code y Codex sin preguntas:

```sh
npx --yes skills add janpereira-dev/helldocs --agent codex claude-code --yes
```

Usamos la herramienta existente [vercel-labs/skills](https://github.com/vercel-labs/skills),
no un paquete npm propio ni un wrapper. Requiere Node.js/npm y Git, no Python.
La instalación predeterminada es por proyecto. `--yes` omite confirmaciones y puede
reemplazar skills existentes del mismo nombre: revise el destino previamente.
Si necesita copias en lugar de enlaces, Skills CLI admite `--copy`.

Mientras GitHub sea privado, se necesita autenticación y acceso al repositorio.
No se cambia su visibilidad como efecto secundario de simplificar la instalación.

## Uso inmediato

Codex: `Usa $helldocs para documentar este proyecto.`

Claude Code: `/helldocs Documenta este proyecto.`

El agente actual aplica la skill, narra y guarda documentación. No necesita Python,
subagentes personalizados, MCP ni API keys adicionales. El helper Python es opcional;
el inventario se puede elaborar con las herramientas de lectura del host.

## Adaptadores opcionales: no incluidos en la instalación estándar

`npx skills add` instala skills; no registra nuestras definiciones de subagente.
Conservamos los adaptadores para usuarios que ya gestionan agentes nativos:

| Adaptador del repositorio | Destino manual opcional | Restricción |
|---|---|---|
| `adapters/codex/helldocs_archivist.toml` | `.codex/agents/helldocs_archivist.toml` | Sandbox `read-only` |
| `adapters/claude/helldocs-archivist.md` | `.claude/agents/helldocs-archivist.md` | `Read, Grep, Glob` |

Solo configure estos agentes si desea delegación separada; no son necesarios para
usar HELLDOCS. No sobrescriba definiciones existentes. La carga real depende del host.

## Límites de seguridad

La skill impone instrucciones de documentación, no una sandbox que limite escrituras
por directorio. Los adaptadores opcionales tienen restricciones distintas y retornan
borradores. El sandbox de archivos tampoco convierte conectores MCP en solo lectura.
No se deben abrir secretos ni ejecutar herramientas mutantes para el reconocimiento.

Skills CLI puede usar enlaces simbólicos entre directorios de skills; esos enlaces
instalados y autorizados son distintos de enlaces encontrados en el código analizado.
La skill sigue sin permitir explorar enlaces del proyecto fuera del alcance autorizado.

## Fuentes verificadas el 2026-09-28

- [Skills CLI: instalación, agentes y repositorios privados](https://github.com/vercel-labs/skills)
- [Skills CLI: documentación](https://skills.sh/docs/cli)
- [Codex: agentes](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Claude Code: subagentes](https://code.claude.com/docs/en/sub-agents)

Publicación en catálogos y validación de comportamiento en clientes son etapas
separadas de la instalación de archivos. No se promete compatibilidad con Cowork
ni con todos los agentes alojados.
