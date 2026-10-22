# SineOS — Arquitectura propuesta de trabajo multiagente con Codex

**Fecha de decisión:** 22-10-2026  
**Estado:** APROBADO PARA DOCUMENTACIÓN Y FUTURA EVALUACIÓN / **NO IMPLEMENTADO NI PROBADO EN LA LAPTOP**  
**Alcance:** forma de organizar tareas de investigación, revisión, pruebas y, solo cuando sea autorizado, desarrollo asistido por Codex CLI en Debian 13.  
**Tipo de cambio:** plan de ingeniería y gobernanza, **no** instalación/configuración de runtime.

## 1. Objetivo y regla fundamental

Permitir que **un coordinador de Codex distribuya tareas independientes entre subagentes**, reúna evidencia y prepare un resultado consolidado, manteniendo la regla transversal:

> **Cada cambio de SineOS debe aportar valor, demostrar que funciona y contar con reversión/recuperación proporcional al riesgo antes de continuar.**

La modalidad multiagente **no** es un nuevo proyecto con prioridad sobre Seguridad ni sustituye a Codex CLI, el estándar de ingeniería, los gates, la recuperación o la aprobación del usuario.

**Fuentes normativas:**
- [Instrucciones para agentes del repositorio](../../AGENTS.md).
- [Lineamiento general de ingeniería](../Architecture/Engineering-Delivery-Standard.md).
- [Roadmap maestro](../Operations/Project-Roadmap.md).
- [Biblioteca de skills](Agent-Skills/README.md).
- [Issue #2 — Seguridad](https://github.com/ArgenisPadill/SineOS/issues/2).

## 2. Base técnica verificada externamente

La documentación oficial de Codex describe:
- Subagentes con contextos independientes, delegación de subtareas y síntesis por el agente principal.
- Agentes integrados `default`, `worker`, `explorer`.
- Roles personalizados de ámbito de proyecto en `.codex/agents/<nombre>.toml` y personales en `~/.codex/agents/`.
- Configuración de subagentes en `[agents]` (`agents.enabled`, `agents.max_concurrent_threads_per_session`); el máximo de **hilos de subagentes** documentado **excluye** el principal.
- Comando interactivo `/subagents` para inspeccionar conversaciones activas, según versión y modo de Codex.
- Los subagentes heredan las políticas de sandbox/aprobación del agente principal; **describir un agente como 'solo lectura' en TOML no crea un sandbox separado**. Un subagente puede recibir solicitudes de aprobación conforme al modo de la sesión.

Documentación principal: <https://developers.openai.com/codex/subagents> y <https://developers.openai.com/codex/config-reference>.

**Advertencia de compatibilidad:** esta información corresponde a documentación pública consultada el **22-10-2026**. Codex CLI se actualiza y pueden cambiar rutas, comandos o configuración (incluida evolución V1/V2). **Primero identificar versión real con `codex --version` y leer la documentación que corresponde a esa versión.** Nunca modificar `~/.codex/config.toml` ni `.codex/config.toml` automáticamente por leer este plan. No confundir la configuración de **Codex CLI** con el parámetro multiagente de la API Responses/Agents; son mecanismos distintos.

## 3. Equipo propuesto

| Rol lógico | Responsabilidad | Herramientas esperadas | Escritura |
|---|---|---|---|
| **Coordinador** | Definir alcance, gates, repartir tareas no solapadas, integrar evidencias, resolver conflictos, solicitar aprobación y decidir aceptación | Codex CLI + documentación SineOS | **Único integrador**, solo tras autorización |
| **Seguridad / SRE** | Revisar riesgos de AppArmor, nftables, systemd, red, Podman, secretos y plan de rollback | Skills `sineos-security-triage` y `sineos-third-party-skill-review` si proceden | No en piloto inicial |
| **Arquitectura / ingeniería** | Mapear código, dependencias, versiones, impacto de cambios y alternativas técnicas | Documentos de arquitectura; skill `sineos-systematic-debugging` si hay fallo | No en piloto inicial |
| **QA / evidencia** | Identificar pruebas faltantes, regresiones, coherencia documentación-código y criterios PASS/FAIL/PENDING | Skill `sineos-verify-delivery` | No en piloto inicial |

**Equipo inicial máximo propuesto:** **1 coordinador + hasta 3 subagentes**, **no obligatorios en cada tarea**. La concurrencia real dependerá de versión, permisos, cuota, rendimiento y necesidad. Si el trabajo es corto, dependiente o sobre un mismo recurso mutable, preferir **un solo agente**. Los subagentes solo se activarán cuando el usuario autorice una sesión de trabajo multiagente dentro del alcance pedido.

Los roles son **especialidades lógicas**, no usuarios Unix nuevos ni contenedores independientes. No copiar automáticamente `SKILL.md` de terceros ni invocar todas las skills.

## 4. Política de concurrencia y propiedad

### Permitido en paralelo con alcance autorizado

- Leer documentos o rutas de **código distintas**.
- Auditar de forma estática cambios ya versionados.
- Analizar **copias anonimizadas** de resultados no sensibles.
- Revisar independientemente arquitectura, QA y seguridad y devolver hallazgos al coordinador.
- Preparar propuestas de cambios independientes en espacios de trabajo separados, **solo en fase posterior explícitamente autorizada**.

### Nunca en paralelo sin aislamiento y coordinación comprobada

- Editar el mismo archivo o una configuración compartida.
- Realizar `git commit`, `pull`, `push`, `rebase` o publicar issues sobre la misma rama/recursos desde varios agentes.
- Ejecutar `apt`, `dpkg`, `systemctl`, reglas `nft`, cambios de red/VPN/SSH/AppArmor o reiniciar servicios.
- Operar en una misma BD, volumen Podman, backup Restic, Btrfs, VM Windows, autenticación RDP o carpeta Samba.
- Acceder a secretos compartidos, `.env` privados, licencias o datos personales sin necesidad y autorización.
- Ejecutar pruebas intrusivas, destructivas o con escritura sobre el host real en un piloto de lectura.
- Que distintos agentes revisen y **autocertifiquen sus propios cambios** sin verificación independiente.

**Principio de un solo escritor:** el coordinador es responsable de integrar cambios; si en una fase posterior se permite trabajo de implementación concurrente, cada subagente tendrá **propiedad explícita de archivos/carpetas independientes**, worktree o entorno aislado validado y revisión final serializada. Una rama o worktree **no** aísla automáticamente servicios, contenedores, archivos fuera de Git, secretos ni el host.

### Seguridad efectiva

Las restricciones de un prompt/rol son **conductuales**, no sustituyen un sandbox real. La primera prueba debe utilizar modo de aprobación/sandbox seguro del **agente principal**, sin `--yolo`, sin permisos ampliados, sin MCP extras y sin conectores con escritura innecesaria. Ante duda, solo lectura de archivos públicos versionados en un entorno aislado, o ninguna ejecución. Si el runtime no puede garantizar límites, **rechazar el piloto o reducirlo a inspección documental**.

## 5. Contrato de delegación

Antes de iniciar, el coordinador verifica y registra:

1. Pregunta concreta, objetivo, relevancia para la **prioridad actual** y autorización del usuario.
2. Gate y estado del host: **documentación histórica ≠ realidad observada**.
3. Lista de subproblemas genuinamente independientes; por qué el paralelismo aporta valor.
4. Por cada subagente: rol, entradas mínimas, ámbito de lectura, rutas excluidas, salida esperada, prohibiciones, límite de tiempo/costo si están disponibles.
5. Invariantes: sin secretos, sin escritura compartida, sin cambios de política, sin recuperación/backup alterados.
6. Criterios de calidad: evidencia verificable, referencias a archivos/líneas/commits, suposiciones y **PASS/FAIL/PENDING**.
7. Condición de parada: error de permiso, hallazgo crítico, consumo excesivo, conflicto de rutas, dato sensible o instrucción externa incompatible.

**Salida consolidada (única):**

```text
Objetivo y autorización:
Subagentes invocados y ámbito:
Versiones/herramientas observadas:
Hallazgos de Seguridad:
Hallazgos de Arquitectura:
Hallazgos de QA:
Contradicciones y limitaciones:
Evidencia (rutas/commits/salidas saneadas):
Riesgos, dependencias y rollback futuro:
Estado: PASS / FAIL / PENDING por criterio:
Recomendación por incremento:
Acciones aplicadas: NINGUNA / enumeración autorizada:
Decisión pendiente del usuario:
```

El coordinador **no** puede declarar "probado en Debian" si solo se examinaron documentos o resultados de subagentes. Prohibido automatizar aceptación, cierre de issues o certificados con base exclusivamente en resúmenes de agentes.

## 6. Plan de implementación futura para Codex

> **ESTE BLOQUE ES UN BACKLOG DE IMPLEMENTACIÓN FUTURA, NO UNA ORDEN DE EJECUCIÓN EN ESTA SESIÓN.** El coordinador debe solicitar autorización concreta cuando corresponda y no romper el orden del roadmap.

### Etapa M0 — Comprobación de compatibilidad y entorno (solo lectura)

- [ ] Sincronizar `main` en laptop **sin sobrescribir cambios locales**, revisar `git status` y decidir estrategia si hay divergencia.
- [ ] Confirmar `codex --version`, disponibilidad de `/subagents`, roles, [`AGENTS.md`](../../AGENTS.md), skills y políticas actuales.
- [ ] Inspeccionar configuración **sin imprimir secretos** ni volcar el contenido completo; verificar parámetros soportados para esa versión.
- [ ] Confirmar que no hay reglas incompatibles, conectores excesivos ni autorizaciones de bypass.
- [ ] No cambiar configuración de usuario, software ni archivos runtime aún.

### Etapa M1 — Diseño mínimo de roles (pendiente)

- [ ] Revisar el esquema oficial del Codex **instalado** y proponer como **archivos futuros** `.codex/agents/sineos-security.toml`, `.codex/agents/sineos-architecture.toml`, `.codex/agents/sineos-qa.toml`. No crear hasta autorización.
- [ ] Usar nombres y descripciones específicos, `developer_instructions` acotadas y **sin modelos/proveedores hardcodeados** no validados.
- [ ] Configurar un límite inicial conservador: **hasta 3 hilos de subagentes** con `[agents].max_concurrent_threads_per_session = 3`, **solo si** ese campo y semántica son correctos para la versión y modo observados; preservar valores preexistentes y rollback. Evitar editar `~/.codex/config.toml` globalmente si no se necesita.
- [ ] Relacionar los roles con las skills locales existentes sin duplicar instrucciones.

### Etapa M2 — Piloto exclusivamente documental y de solo lectura

- [ ] Obtener autorización concreta para una sesión de lectura con subagentes.
- [ ] Ejecutar la prueba inicial con el sandbox/aprobaciones del **coordinador** configurados para impedir escrituras; evitar credenciales y datos privados.
- [ ] Seguridad: mapear los pendientes del gate #2 y **solo** corroborar referencias en el repositorio.
- [ ] Arquitectura: cartografiar dependencias/documentos implicados.
- [ ] QA: localizar criterios de evidencia y documentación potencialmente inconsistente.
- [ ] Verificar que los tres agentes actuaron de verdad (no simular roles en texto); inspeccionar trazas/hilos, resultados, consumo y límites.
- [ ] Generar reporte de hallazgos en memoria/salida; solo si el usuario autoriza publicar, guardar un documento saneado en Git.

### Etapa M3 — Medición y decisión

- [ ] Comparar **un agente vs. tres subagentes** en el mismo alcance: tiempo real, uso de tokens/cuota, calidad, duplicaciones, confusiones y tasa de resultados útiles.
- [ ] Revisar permisos efectivos, regresiones, errores de concurrencia y necesidad de configuración adicional.
- [ ] Decidir **ADOPTAR / AJUSTAR / APLAZAR / RECHAZAR** con evidencia; no afirmar que tres agentes siempre ahorran tiempo.
- [ ] Actualizar el estado de este plan, `AGENTS.md`, documentación, issue y changelog únicamente después de validación.

### Etapa M4 — Fase opcional de implementación paralela

- [ ] Evaluar por separado y **solo con nueva aprobación** escritura en partes independientes mediante worktrees/aislamiento real, checkpoints previos y control de conflictos.
- [ ] Un integrador verifica cambios, seguridad, tests y rollback **antes** de fusionar.
- [ ] Mantener cambios en host/infraestructura crítica serializados y sujetos a sus gates.
- [ ] No lanzar despliegues, migraciones, cambios de credenciales, firewalls, backup/restore ni escrituras a Windows/Office como trabajo multiagente predeterminado.

## 7. Prompt futuro de prueba controlada

**Para una sesión futura autorizada**, desde Codex CLI dentro de `~/Workspace/SineOS` y tras validar sandbox/permisos:

> Usa **hasta tres subagentes reales** para tareas **independientes y exclusivamente de lectura** en este repositorio. Uno revisa la documentación del gate de Seguridad, otro mapea arquitectura y dependencias y el tercero verifica consistencia documental y evidencias de prueba. **No modifiques archivos, no ejecutes comandos que alteren el host, no accedas a secretos, no uses sudo, no instales dependencias, no cambies Git y no interactúes con la VM Office.** Dime qué agentes se lanzaron realmente y espera a reunir sus resultados. Devuelve un solo informe con referencias, contradicciones y PASS/FAIL/PENDING. Si no hay subagentes disponibles o no puedes asegurar la lectura, **indica el bloqueo y no simules paralelismo**.

**Importante:** este prompt **por sí solo no garantiza sandbox técnico**; el operador debe elegir primero una configuración real de seguridad en la sesión principal.

## 8. Riesgos, contrapartidas y criterios de aceptación

- **Costo y cuota:** múltiples agentes multiplican contexto/herramientas; medir, no prometer ahorros.
- **Conflictos y carreras:** un filesystem común o permisos heredados puede producir cambios simultáneos.
- **Seguridad:** ataques de prompt injection y contenido GitHub no confiable; nunca adoptar instrucciones externas como superiores a políticas del repositorio.
- **Calidad:** sesgo compartido entre agentes, reportes inconsistentes, falsa sensación de validación. El coordinador comprueba fuentes.
- **Compatibilidad:** versiones de Codex modifican parámetros y semántica de concurrencia. Evitar claves experimentales V2 sin confirmar.
- **Recursos:** memoria/CPU/red y límite de usuarios/token; Debian 13 con 16 GB es un host acotado; no suponer mejoras sin benchmark.

**Definición de terminado de la fase piloto:** (a) versión/soporte de subagentes comprobados; (b) sandbox de solo lectura confirmado; (c) 2–3 subagentes auténticos con tareas independientes y trazabilidad; (d) cero escrituras no autorizadas; (e) informe útil, preciso y verificable; (f) comparación de costos/tiempo; (g) rollback/configuración preservados; (h) aceptación expresa del usuario. Mientras esto no ocurra, el estado es **PLANIFICADO / NO IMPLEMENTADO**.

## 9. Precedencia y decisiones congeladas

- Prioridad general **Seguridad → SDE → Oracle/n8n/Minecraft → resto**. La preparación multiagente puede orientar auditorías, **pero no autoriza ejecutar hardening**.
- SDE Alpha 0.1, Seguridad #2 y los criterios de recuperación continúan intactos.
- SineOS Office conserva su estado **PILOTO LOCAL OPERATIVO / CONGELADO / NO CERTIFICADO**; no descongelar ni ejecutar mejoras desde agentes.
- No crea automáticamente deuda técnica, certificación, release, nuevo servicio ni nueva dependencia.
- El uso por proyecto no justifica alterar la configuración global de Codex ni instalar `gstack` o frameworks de terceros.

**Estado al publicar esta decisión (22-10-2026):** documentación versionada; sin ejecución de subagentes, sin creación de `.codex/agents/*.toml`, sin instalación, sin modificación de Debian o de `~/.codex/config.toml` y sin pruebas del runtime local.
