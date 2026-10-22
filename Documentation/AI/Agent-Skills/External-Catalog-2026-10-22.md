# Catálogo investigado de Agent Skills de terceros para SineOS

**Corte de investigación:** 22-10-2026 (GitHub público y documentación oficial consultados).  
**Estado de TODOS los registros:** **CANDIDATOS EXTERNOS, NO INSTALADOS, NO AUDITADOS EXHAUSTIVAMENTE**. Haber leído `README`/`SKILL.md` y localizado la ruta **no certifica la seguridad de los scripts** ni su comportamiento en Debian 13/Codex.

## Criterios de selección

SineOS usa Debian 13, XFCE/X11, Podman rootless, systemd, nftables, AppArmor, Btrfs/Restic, PostgreSQL, Miyo/Ollama, GitHub y herramientas de desarrollo. Se valoró: utilidad real, especificidad del disparador, origen, instrucciones transparentes, control de permisos, evidencia, rollback y posibilidad de evaluación **sin ejecutar código ajeno**. Prioridad **P1 = investigar antes**, **P2 = futura evaluación**, **P3 = solo referencia**. Ninguna prioridad supone instalación o permiso operativo.

## 1. Seguridad, Debian y recuperación

| Prioridad | Skill (ruta verificada) | Fuente | Uso propuesto en SineOS | Advertencia |
|---|---|---|---|---|
| **P1** | [Debian Linux Triage](https://github.com/github/awesome-copilot/blob/main/skills/debian-linux-triage/SKILL.md) | `github/awesome-copilot` | AppArmor, APT/dpkg, systemd, diagnósticos Debian 13 | Sugiere remedios y comandos: usar solo diagnóstico hasta aprobación |
| **P1** | [Differential Review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md) | `trailofbits/skills` | Revisar diferencias de nftables, scripts, seguridad y alcance de impacto | Instrucciones con acceso a shell; adaptar a solo lectura |
| **P1** | [GitHub Actions Hardening](https://github.com/github/awesome-copilot/blob/main/skills/github-actions-hardening/SKILL.md) | `github/awesome-copilot` | Revisar permisos `GITHUB_TOKEN`, acciones no fijadas, entradas no confiables | No agregar pipelines automáticos sin gate |
| **P1** | [Agentic Actions Auditor](https://github.com/trailofbits/skills/blob/main/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SKILL.md) | `trailofbits/skills` | Riesgo de prompt injection en GitHub Actions que ejecutan IA | Es auditoría estática, no prueba de explotación |
| **P1** | [MCP Security Audit](https://github.com/github/awesome-copilot/blob/main/skills/mcp-security-audit/SKILL.md) | `github/awesome-copilot` | Configuración de servidores MCP, versiones fijadas, secretos, argumentos | No conectar MCP externos sin revisar privilegios |
| **P1** | [Agent Supply Chain](https://github.com/github/awesome-copilot/blob/main/skills/agent-supply-chain/SKILL.md) | `github/awesome-copilot` | Manifiestos de integridad SHA-256 y procedencia de skills/plugins | La verificación de hashes no implica ausencia de malware |

## 2. Ingeniería, depuración y pruebas

| Prioridad | Skill | Fuente | Uso propuesto | Advertencia |
|---|---|---|---|---|
| **P1** | [Systematic Debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) | `obra/superpowers` | Reproducir, investigar causa raíz y evitar parches acumulados | Su metodología no autoriza cambios al host |
| **P1** | [Verification Before Completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) | `obra/superpowers` | No marcar PASS ni cerrar issues sin evidencia actual | Adaptar a pruebas de host vs. validación estática |
| **P1** | [Test Gap Audit](https://github.com/github/awesome-copilot/blob/main/skills/test-gap-audit/SKILL.md) | `github/awesome-copilot` | Detectar pruebas de regresión faltantes, cobertura débil | Auditoría de pruebas; no modifica por defecto |
| **P2** | [Writing Plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) | `obra/superpowers` | Dividir SDE y hardening en incrementos con criterios de aceptación | No copiar ubicaciones `docs/superpowers/` sin adaptar |
| **P2** | [Test Driven Development](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md) | `obra/superpowers` | Funciones de aplicaciones SineOS con pruebas unitarias | Metodología estricta; no siempre adecuada para configuración/firmware |
| **P2** | [PostgreSQL Code Review](https://github.com/github/awesome-copilot/blob/main/skills/postgresql-code-review/SKILL.md) | `github/awesome-copilot` | Revisar funciones/consultas, esquema y seguridad de PostgreSQL 18 | Revisiones, no migraciones ejecutadas |

## 3. Documentación, gobernanza y conocimiento

| Prioridad | Skill / proyecto | Fuente | Uso propuesto | Advertencia |
|---|---|---|---|---|
| **P1** | [Docs Sync Audit](https://github.com/github/awesome-copilot/blob/main/skills/docs-sync-audit/SKILL.md) | `github/awesome-copilot` | Detectar documentación desactualizada frente a código/configuración | No reescribir documentación sin evidencia |
| **P2** | [Acquire Codebase Knowledge](https://github.com/github/awesome-copilot/blob/main/skills/acquire-codebase-knowledge/SKILL.md) | `github/awesome-copilot` | Mapear arquitectura, servicios, dependencias y código para Codex | Contiene scripts Python: auditar antes de ejecutar |
| **P2** | [Superpowers (marco completo)](https://github.com/obra/superpowers) | `obra/superpowers` | Inspiración en planear→probar→revisar y subagentes | Amplio/imperativo; evitar conflicto con `AGENTS.md` SineOS |
| **P2** | [gstack](https://github.com/garrytan/gstack) | `garrytan/gstack` | Revisión de ingeniería/QA/diseño y roles virtuales | Ecosistema grande, permisos/herramientas extra y riesgo de sobrecarga; evaluar selectivamente |
| **P2** | [Web Design Guidelines](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) | `vercel-labs/agent-skills` | Revisar interfaces web SineOS (no sustituye guías GTK) | Consulta reglas remotas cambiantes; fijar referencia antes de adoptar |
| **P3** | [Anthropic Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | `anthropics/skills` | Inspiración para crear/evaluar skills, no requisito con Codex | Licencia de cada skill puede ser distinta; NO copiar sin revisar |
| **P3** | [OpenAI Skills (histórico)](https://github.com/openai/skills) | `openai/skills` | Referencia histórica del formato Agent Skills | Repositorio declarado **deprecated**; priorizar documentación oficial actual |

## 4. Fuentes para seguimiento, NO para instalar en bloque

- [`github/awesome-copilot`](https://github.com/github/awesome-copilot/tree/main/skills): biblioteca de skills por tarea; usar rutas individuales, verificar scripts y licencias.
- [`trailofbits/skills`](https://github.com/trailofbits/skills): auditoría y seguridad, algunas habilidades pensadas para Claude; comprobar integración real con Codex. Repositorio con licencia **CC-BY-SA-4.0**, no incorporar código/instrucciones como propias sin revisar.
- [`obra/superpowers`](https://github.com/obra/superpowers): metodología y skills reutilizables; la instalación total puede introducir demasiadas reglas simultáneas.
- [`VoltAgent/awesome-agent-skills`](https://github.com/VoltAgent/awesome-agent-skills): índice curado, **no auditoría de seguridad**. Útil como buscador, no instalar por volumen.
- [`JPeetz/agent-skills`](https://github.com/JPeetz/agent-skills): catálogo transversal (DevOps, SRE, seguridad, documentación); autor declara evaluaciones propias, sin que SineOS las haya corroborado.
- [Guía oficial OpenAI para crear skills](https://developers.openai.com/plugins/build/skills): estructura y frontmatter `SKILL.md`.
- [Documentación oficial de GitHub sobre Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills): rutas `.agents/skills`, scope y requisitos.

## Resultado de la investigación

1. **Publicar skills propias mínimas** en `.agents/skills/`, adaptadas a la filosofía SineOS, sin scripts, sin autoinstaladores y sin dependencia de internet.
2. **Mantener este catálogo como fuente de candidatos**. No convertir enlaces en comandos ejecutables, ni clonar repositorios para ejecutarlos con privilegios.
3. **Adoptar una skill externa únicamente después del protocolo de seguridad**: revisión de código, licencia, versiones, recursos, conflictos de instrucciones, sandbox y pruebas.
4. Empezar por auditoría de Seguridad tras decisión explícita, sin interrumpir el roadmap ni reabrir el piloto SineOS Office.
5. Actualizar este catálogo cuando se revisen los repositorios o cambien sus licencias/funciones; no afirmar actualizaciones automáticas.

**Pruebas completadas en esta investigación:** existencia de los archivos `SKILL.md` señalados y lectura selectiva de su alcance declarado. **No completadas:** auditoría exhaustiva de cada dependencia/script, prueba del Codex instalado, compatibilidad real con Debian, benchmark y revisión completa de todas las licencias.
