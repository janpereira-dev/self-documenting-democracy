# Contrato del expediente

## Salida por defecto

Dentro de `docs/super-earth/`:

- `README.md`: apertura del Portavoz, propósito real, alcance, snapshot e índice.
- `architecture.md`: mapa del superdestructor, componentes, límites, decisiones
  verificadas y diagramas de dependencias.
- `modules/`: un expediente por módulo significativo; no uno por archivo trivial.
- `flows.md`: recorridos principales, errores, sincronía y efectos secundarios.
- `data.md`, `interfaces.md`, `integrations.md`: solo si existen esos frentes.
- `operations.md`: arranque, configuración por nombre, CI/CD declarado, pruebas
  existentes, comandos documentados pero no ejecutados, observabilidad y recuperación.
- `unknowns.md`: contradicciones, inferencias, riesgos sustentados y pendientes.
- `coverage.json`: inventario ampliado y estado de lectura/documentación.
- `evidence.md`: registro navegable de fuentes técnicas.
- `assets/`: insignias utilizadas, copiadas localmente.

En un proyecto pequeño combina capítulos; conserva índice, evidencia y cobertura.
No generes páginas vacías solo para cumplir esta lista.

## Expediente de módulo

1. Portavoz — apertura ficticia breve.
2. Misión — responsabilidad y límites con nombre real.
3. Coordenadas — rutas y símbolos.
4. Entradas/salidas — tipos, contratos, validación y errores.
5. Maniobra — flujo verificado y dependencias.
6. Riesgos y límites — hechos, inferencias y cuestiones abiertas separadas.
7. Pruebas — archivos y casos existentes; ejecución no realizada si aplica.
8. Muestras — enlaces a fuentes y evidencias.
9. Orden siguiente — lectura o verificación recomendada, no reparación automática.

## Evidencia

Asigna IDs `E-001`, etc. Cada afirmación importante apunta a un ID con ruta relativa,
símbolo o líneas realmente inspeccionadas, snapshot y explicación. Enlaces de archivo
relativos al documento; el rango de líneas se escribe también en texto para lectores
que no soporten fragmentos `#L10-L20`. No uses un enlace inexistente para aparentar rigor.

Estados de afirmación: `observed`, `inferred`, `unknown`, `contradicted`.
Comentarios y README pueden estar obsoletos: informa discrepancias con implementación,
no elijas silenciosamente el texto más conveniente. Lo observado está limitado al
snapshot: no equivale a verificación de producción.

## Cobertura honesta

El helper entrega `entries` con `path`, `kind`, `status`, `reason` y metadatos.
Conserva su inventario y añade `read_ranges`, `evidence_ids`, `document`, `documented`.
Estados de archivo: `pending`, `read`, `partial`, `excluded`, `blocked`.
Las carpetas podadas constan como UNA entrada de directorio: no cuentan como archivos
leídos ni se conoce la cantidad de archivos interiores. No las elimines del informe.

Reporta por separado:
- archivos candidatos inventariados;
- leídos completamente / parciales / pendientes / bloqueados;
- archivos y directorios excluidos con motivos;
- módulos documentados y no aplicables;
- errores de inventario y rutas fuera de alcance.

Si usas porcentaje: `read / (read + partial + pending + blocked)` entre archivos
candidatos, con denominador explícito. Denominador cero significa `not_applicable`,
no 100 %. `documented` y `read` son dimensiones diferentes. No proclames haber leído
todo el proyecto si hay carpetas excluidas, errores, archivos parciales o pendientes.

## Continuidad

En proyectos grandes guarda avances por lote dentro del destino documental:
snapshot, sectores completados, cola pendiente y próximo archivo/rango. Si cambian
las fuentes, marca stale la evidencia afectada y relee antes de reutilizarla.
La documentación previa no sustituye leer el código de una nueva revisión.

## Límites técnicos de protección

La skill define un contrato de escritura documental, NO una sandbox por extensión.
El agente nativo del paquete sí solicita sandbox `read-only`; devuelve borradores
en su respuesta. El orquestador es quien escribe y debe verificar el destino.
El sandbox de archivos no implica que un conector MCP remoto sea de solo lectura:
el agente no debe invocar herramientas mutantes, aunque estén disponibles.
