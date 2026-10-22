# SineOS — Biblioteca de habilidades de agentes de IA

**Fecha de investigación:** 22-10-2026  
**Estado:** REFERENCIA VERSIONADA + SKILLS NATIVAS DOCUMENTALES; NO INSTALACIÓN EXTERNA  
**Ámbito:** desarrollo, seguridad, auditoría, pruebas, documentación, recuperación, automatización y administración de SineOS con Codex y otros agentes compatibles.

## Propósito

## Orquestación multiagente — desarrollo futuro

Codex puede distribuir tareas entre subagentes, mientras las **skills** contienen instrucciones especializadas. No son la misma función. La [propuesta multiagente de SineOS](../Multiagent-Codex-Planning.md) define roles, seguridad, fases futuras, prueba inicial de lectura, mediciones y la relación con las skills nativas; [issue #11](https://github.com/ArgenisPadill/SineOS/issues/11). **Estado: PLANIFICADO / NO CONFIGURADO NI PROBADO.** No se autoriza ningún lanzamiento de agentes por esta referencia.

Mantener en GitHub un lugar estable y rastreable para **descubrir, evaluar y aprovechar habilidades de IA** sin saturar de instrucciones al agente ni comprometer Debian. No supone adopción técnica de proyectos externos ni modifica el roadmap.

### Punto de entrada para Codex

1. Leer el [lineamiento obligatorio de ingeniería](../../Architecture/Engineering-Delivery-Standard.md) y [AGENTS.md](../../../AGENTS.md).
2. Consultar este índice y el [catálogo externo curado](External-Catalog-2026-10-22.md).
3. Cuando corresponda a la petición, utilizar las **skills nativas de SineOS** en [`.agents/skills/`](../../../.agents/skills/); cada una tiene un `SKILL.md` y un alcance específico.
4. Para cualquier skill de terceros, seguir el [protocolo de evaluación y adopción](Skill-Adoption-Protocol.md). El catálogo **no** constituye autorización para ejecutar, descargar o instalar.
5. Respetar los gates: **Seguridad → SDE → Oracle/n8n/Minecraft → reproducibilidad → SLDE**, las decisiones congeladas y los permisos explícitos del usuario.

## Habilidades nativas disponibles en el repositorio

| Skill | Objetivo | Tipo | Estado |
|---|---|---|---|
| [sineos-security-triage](../../../.agents/skills/sineos-security-triage/SKILL.md) | Inventarios y auditoría defensiva inicial de Debian 13 sin modificar el host | Solo lectura | Publicada; ejecución real en Codex pendiente de probar |
| [sineos-systematic-debugging](../../../.agents/skills/sineos-systematic-debugging/SKILL.md) | Reproducción de errores, hipótesis, causa raíz y propuesta de corrección reversible | Solo diagnóstico por defecto | Publicada; ejecución real pendiente |
| [sineos-verify-delivery](../../../.agents/skills/sineos-verify-delivery/SKILL.md) | Evidencia PASS/FAIL/PENDING antes de declarar terminado un cambio | Verificación / informe | Publicada; ejecución real pendiente |
| [sineos-third-party-skill-review](../../../.agents/skills/sineos-third-party-skill-review/SKILL.md) | Revisar procedencia, permisos, scripts, licencias y compatibilidad de skills | Evaluación, no instalación | Publicada; ejecución real pendiente |

Son instrucciones **originales específicas de SineOS**, inspiradas en principios públicos examinados; no son una copia ni un instalador de skills ajenas. Ninguna ejecuta comandos al aparecer en el catálogo. Los agentes solo actúan conforme a la autorización efectiva de la tarea.

## Qué se recomienda evaluar primero

**Prioridad de investigación post-gate de Seguridad:**
- [GitHub — Debian Linux Triage](https://github.com/github/awesome-copilot/blob/main/skills/debian-linux-triage/SKILL.md), para complementar la auditoría de AppArmor/systemd/apt (sin aplicar sus remedios automáticamente).
- [obra — Systematic Debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) y [Verification Before Completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md).
- [Trail of Bits — Differential Review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md).
- [GitHub — Agent Supply Chain](https://github.com/github/awesome-copilot/blob/main/skills/agent-supply-chain/SKILL.md).

**No adoptar todas a la vez:** primero comparar si las skills locales ya satisfacen la necesidad y seleccionar una capacidad externa adicional solo con beneficio claro.

## Instalación, descubrimiento y límites

La documentación actual de Codex y de GitHub reconoce las skills de proyecto en `$REPO_ROOT/.agents/skills/<nombre>/SKILL.md`. Tras sincronizar el repositorio con Debian, iniciar Codex desde la raíz de SineOS y consultar `/skills` o invocar `$sineos-security-triage` (cuando la versión instalada lo soporte). **La detección en la laptop y la compatibilidad de la versión real de Codex aún no han sido comprobadas.**

Las skills activas son solo reglas de trabajo; **no añaden capacidades de sistema, conectores, paquetes, permisos ni acceso fuera de las herramientas que Codex ya tiene**. Un enlace a GitHub no equivale a una skill instalada.

**Gobernanza:** [Estándar SineOS](../../Architecture/Engineering-Delivery-Standard.md) · [Catálogo curado](External-Catalog-2026-10-22.md) · [Adopción](Skill-Adoption-Protocol.md) · [Roadmap](../../Operations/Project-Roadmap.md).

**Estado de esta incorporación:** solo cambios documentales/versionados en GitHub. Ningún script externo descargado o ejecutado, ninguna nueva integración MCP, ninguna modificación del host, de Windows, de Office o de los respaldos.
