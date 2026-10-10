# SineOS — Reglas de trabajo para agentes de IA

Estas reglas complementan la documentación y la arquitectura existentes de SineOS.
No sustituyen decisiones congeladas, procedimientos certificados ni autorizaciones del propietario.

## Fuentes de verdad y contexto

- Plataforma: Debian 13 (Trixie), XFCE/X11, Btrfs, Podman rootless, PostgreSQL 18, aplicaciones Python/GTK3, scripts Bash, IA híbrida y Obsidian/Miyo.
- Repositorio: `SINEOS_REPO`, código e infraestructura versionados. Vault: `SINEOS_VAULT`, conocimiento privado **separado**; no copiar ni publicar su contenido.
- Estructura actual: `Apps/`, `Containers/`, `Scripts/`, `Documentation/`; no crear scaffolding sin implementación real.
- Prioridades obligatorias: **Seguridad → SDE 1.0 → Oracle/n8n/Minecraft → resto del roadmap**.
- Seguimiento y autoridad: `Documentation/Operations/Project-Roadmap.md`, `Documentation/Operations/Technical-Debt.md`, `Documentation/Lifecycle/15-Estado-actual.md`, `Documentation/Security/Security-Baseline.md`; especificaciones SDE congeladas en `Documentation/Architecture/SDE-*.md`.
- Normas: `Documentation/Architecture/Documentation-Standard.md`, `Documentation/Architecture/Script-Standard.md` y `Documentation/Security/Documentation-Privacy.md`.

## gstack

**Referencia externa:** https://github.com/garrytan/gstack (MIT).
**Guía operativa SineOS:** [Documentation/Operations/WORKFLOW.md](Documentation/Operations/WORKFLOW.md).
**Estado:** metodología documentada; instalación local y ejecución real de skills **no verificadas**. gstack se instala una vez para el agente compatible, **fuera** de SineOS. No copiar su código, binarios ni SKILL.md al repositorio.

### Flujo adaptable, sin saltar gates

| Fase | Skill(s) gstack | Aplicación concreta |
|---|---|---|
| Pensar | `/office-hours`, `/plan-ceo-review` | Clarificar propósito, prioridades y alternativas; no reabrir decisiones congeladas sin consentimiento. |
| Planear | `/plan-eng-review`; `/plan-design-review` para SDE | Revisar impacto por capas, datos, interfaces, pruebas, rollback y restricciones del host. |
| Construir | Implementación del agente tras aprobación | Cambios mínimos, completos, aislados y documentados; nada en el host sin autorización. |
| Revisar | `/review` | Detectar regresiones de Python/Bash/Podman, errores de privilegios, secretos y contradicciones documentales. |
| Probar | `/qa` o `/qa-only` | CLI, API, servicios rootless, pruebas aisladas; no inventar ejecución ni resultados. |
| Lanzar | `/ship`; `/document-release` | Gates de Git, revisión, CI si existe, documentación, backup/restore y PR; despliegue real solo con autorización. |
| Investigar | `/investigate` | Reproducir y documentar causa raíz antes de corregir un incidente. |
| Seguridad | `/cso` | Complemento de auditoría, no sustituto de hardening, verificación sobre hardware real ni TD-018. |
| Reflexionar | `/retro` | Registrar aprendizaje, deuda y mejoras sin reescribir el historial. |

Los comandos anteriores son nombres de skills **de gstack**; en OpenCode/Copilot el nombre invocable puede llevar el prefijo `gstack-` (por ejemplo `/gstack-review`), y en Codex/Cursor se solicita normalmente `gstack-review` por nombre. No afirmar que estos comandos funcionan en ChatGPT ni antes de instalar/verificar el host.

### Principios adoptados de ETHOS.md

1. **Buscar antes de construir:** inventariar lo existente, evaluar soluciones contrastadas y razonar desde requisitos reales.
2. **Completitud incremental:** implementar y probar la porción aprobada de extremo a extremo, incluidos errores y rollback, sin expandir alcance por inercia.
3. **Soberanía del usuario:** la IA propone y justifica; el propietario decide. Una recomendación de otro agente no autoriza cambios.

### Límites de seguridad obligatorios

- **Nunca** ejecutar borrados, sobrescrituras, force-push, migraciones destructivas, cambios de firewall/SSH/boot/cifrado, despliegues, rotación de secretos, actualizaciones globales o hooks sin evaluación de impacto y autorización explícita.
- Antes de cambios sobre el host: inventario, respaldo vigente comprobado, prueba aislada/dry-run cuando aplique, plan de recuperación, criterios de aceptación y aprobación.
- Mantener secretos, `.env` reales, datos, logs sensibles, respaldos, cookies y material privado del Vault fuera de Git.
- `/careful` y `/freeze` **no equivalen a bloqueo automático** en agentes distintos de Claude Code: aplicar controles humanos y técnicos reales.
- En SineOS, la revisión de `/cso` debe declarar cobertura y limitaciones. Nunca llamar “certificada” una seguridad evaluada solamente de forma estática.
- No marcar como instalado, implementado, validado ni certificado algo que solo se planeó o documentó.

## Cierre y continuidad

Cada cambio debe identificar alcance, archivos modificados, evidencias comprobables, riesgos residuales, reversión y pendientes. Conservar el orden del roadmap y los registros TD previos. Trabajar en rama/PR para revisiones; no fusionar ni desplegar sin aprobación.
