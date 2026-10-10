# SineOS — WORKFLOW de ingeniería asistida con gstack

**Fecha:** 09-10-2026  
**Tipo:** política de proceso y operación, no instalación.  
**Estado:** documentación propuesta en rama; gstack **no instalado ni certificado** en el host SineOS por este cambio.  
**Referencia:** [garrytan/gstack](https://github.com/garrytan/gstack) (MIT), especialmente `README.md`, `ETHOS.md`, `ARCHITECTURE.md`, `AGENTS.md`.

## 1. Decisión arquitectónica

SineOS adopta el esquema **Pensar → Planear → Construir → Revisar → Probar → Lanzar → Reflexionar** como metodología de desarrollo, **no** como nuevo servicio residente, orquestador de sistema operativo ni cambio de arquitectura. Los roles de gstack son perspectivas de revisión; no conceden autoridad de ejecución.

La instalación de gstack, si se autoriza y reúne requisitos, se realiza **una sola vez fuera del repositorio**, en la configuración del agente local compatible. Este repositorio solo conserva la referencia y su propio contrato operativo en `AGENTS.md`. No vendorizar `SKILL.md`, bibliotecas, binarios, navegador ni dependencias de gstack.

### Estructura real de SineOS

| Dominio | Implementación y contrato a respetar | Validación esperada |
|---|---|---|
| `Apps/` | Python 3; NetworkPrivacy y SineOS Mantenimiento; interfaces GTK3/PyGObject donde aporten valor. | Sintaxis, pruebas de funciones, flujos GUI/CLI en entorno controlado; privilegios mínimos. |
| `Scripts/` | Bash, auditoría y automatizaciones catalogadas. | `bash -n` y validación funcional segura por caso; no modificar el host por defecto. |
| `Containers/` | Podman **rootless**; PostgreSQL, Open WebUI, Stirling PDF, Uptime Kuma; secretos/volúmenes fuera de Git. | Revisar Compose, red, volúmenes, límites de exposición, backup y restore aislados. |
| `Documentation/` | Architecture, Operations, Lifecycle, Security, Recovery. | Consistencia de fuentes de verdad; separar plan/evidencia/estado real. |
| IA y Vault | Obsidian/Miyo; Ollama local y proveedores cloud según política vigente. | Vault privado independiente; no procesar ni publicar secretos/notas privadas sin permiso. |
| SDE | XFCE/X11, LightDM, planes congelados y certificación C0–C12. | **No iniciar implementación física antes de concluir el gate de Seguridad.** |

No sustituir componentes por el simple hecho de que una skill favorezca otro stack. No introducir servicios, agentes residentes, privilegios o consumo de recursos sin justificarlo frente al hardware objetivo.

## 2. Orden maestro: no modificarlo

`Documentation/Operations/Project-Roadmap.md` e issue #4 determinan:
1. **Seguridad** (issue #2): hardening tradicional, evidencia de host, riesgos, rollback, TD-018 al final.
2. **SDE 1.0** (issue #1): plan congelado; implementación y certificación pendientes.
3. **Oracle Cloud / n8n / Minecraft** (issue #5): estudio e implementación únicamente después del gate SDE.
4. **Resto**: reproducibilidad y deuda, SLDE, módulos y laboratorios según roadmap.

Los acuerdos históricos, cierres certificados y deuda técnica permanecen vigentes. La adopción metodológica no crea un reinicio, una migración de arquitectura ni un nuevo orden de prioridades.

## 3. Flujo de trabajo y entregables

| Paso | Skill original de gstack | Entregable y criterio de salida SineOS |
|---|---|---|
| **Pensar** | `/office-hours` y opcional `/plan-ceo-review` | Problema real, alcance, restricciones, alternativas (incluida no construir), decisión del propietario. |
| **Planear** | `/plan-eng-review`; `/plan-design-review` solo si afecta interfaz | Mapa de componentes existentes, dependencias, amenazas, interfaces, fallas, matriz de pruebas y rollback. |
| **Construir** | Implementación del agente elegido, tras aprobar alcance | Cambio autocontenido en `Apps/`, `Scripts/` o `Containers/`; pruebas y docs junto al cambio. |
| **Revisar** | `/review` | Hallazgos priorizados por impacto, diffs acotados, riesgo de regresión, secretos y dependencias. |
| **Probar** | `/qa` (con reparaciones autorizadas) o `/qa-only` (solo informe) | Evidencia real de pruebas ejecutadas, resultados y limitaciones; no pruebas inventadas. |
| **Lanzar** | `/document-release`, `/ship` | Estado Git, documentación, pruebas, escaneo de secretos, PR. Merge/deploy solo tras permiso y gates. |
| **Reflexionar** | `/retro` | Incidencias, lecciones, mejoras y pendientes trazables; no cerrar deuda sin evidencia. |
| **Investigar incidentes** | `/investigate` | Síntomas, reproducción, causa raíz, corrección propuesta, test de regresión y rollback. |
| **Seguridad transversal** | `/cso`, `/careful`, `/freeze` | Auditoría como evidencia auxiliar; consentimiento y aislamiento reales antes de cambios peligrosos. |

Los nombres de esta tabla son **nombres originales**; cada host puede exponerlos con prefijo `gstack-` o mediante solicitud por nombre. Confirmar con `./setup --status` y el catálogo real del agente. No asumir compatibilidad ni ejecución por disponer de `AGENTS.md`.

### Gates de seguridad por clase de cambio

| Clase | Ejemplos | Regla |
|---|---|---|
| Lectura/documentación | Revisar arquitectura, plan o diff sin mutaciones operativas. | Inspección y propuesta; preservar archivos existentes. |
| Código sin privilegios | Pruebas unitarias Python, documentación, diagnóstico local, cambios en rama. | Revisar diff, correr pruebas aisladas y preparar PR. |
| Infraestructura y host | nftables/Podman, SSH, AppArmor, LUKS, actualización de imágenes, respaldos, Btrfs, servicios, sesión LightDM/XFCE. | **Pedir autorización explícita antes de aplicar**; inventario, backup verificado, rollback, ventana de intervención, validación real. |
| Secretos, datos y recuperación | `.env`, credenciales, restauraciones, migraciones SQL, cookies, Vault. | Minimizar exposición, no publicar, consentimiento específico, proceso de recuperación controlado. |

No ejecutar `/ship` suponiendo que equivale a un despliegue libre de riesgos. No ejecutar `/land-and-deploy` ni alterar producción sin autorización explícita. En agentes distintos de Claude Code, `/careful` y `/freeze` son **advisory**, no bloqueos garantizados.

**Alcance real de `/cso`:** la documentación upstream distingue auditoría estática de pruebas de runtime/scanners cualificados. Un reporte estático no satisface TD-018 ni sustituye evidencia sobre la laptop.

### Matriz mínima de validación

- **Python:** imports/sintaxis, pruebas unitarias de rutas nuevas, simulación/mock de llamadas privilegiadas; GUI manual si afecta GTK.
- **Bash:** `bash -n`, lint si está disponible, dry-run o VM aislada antes de scripts que muten sistema.
- **Podman/PostgreSQL:** definición y cambios de redes, permisos y datos revisados; test de recuperación solamente en destino temporal aislado.
- **Seguridad:** alcance, amenazas, exposición de puertos, secretos, evidencia del host y revalidación, no solo informes de IA.
- **SDE:** exigir fases y evidencias del roadmap específico, Definition of Done y certificaciones C0–C12; no iniciar mientras gate Seguridad siga abierto.
- **Documentación:** rutas existentes, enlaces válidos, estados correctos, fecha y fuente de verdad; no elevar “planeado” a “validado” por escribir Markdown.

## 4. ETHOS adoptado (con límites de SineOS)

### Investigar antes de crear

Consultar primero el código y documentación de SineOS, librerías/plataformas existentes y alternativas maduras. Justificar construir, adaptar, sustituir, posponer o descartar. Las tendencias externas no sobreescriben restricciones de SineOS.

### Completar la unidad de trabajo aprobada

Un incremento debe abarcar casos normales, errores, tests aplicables, seguridad, documentación y reversión. Avanzar por unidades pequeñas hasta lograr completitud; **no** usar “hacerlo completo” para añadir alcance no solicitado, romper decisiones congeladas o desplegar sin permisos.

### Soberanía del propietario

El agente plantea opciones, argumentos y riesgos. La decisión humana prevalece, incluso si varios agentes recomiendan otra cosa. Documentar desacuerdos y solicitar consentimiento antes de cambiar la dirección acordada.

## 5. Fuentes de verdad, trazabilidad y cierre

1. Roadmap/prioridades: `Documentation/Operations/Project-Roadmap.md`, issue #4.
2. Deuda abierta/cierre: `Documentation/Operations/Technical-Debt.md`.
3. Estado del sistema: `Documentation/Lifecycle/15-Estado-actual.md`.
4. Seguridad: `Documentation/Security/Security-Baseline.md` y sus políticas.
5. Recuperación: `Documentation/Recovery/Disaster-Recovery.md` y `Backup-Status.md`.
6. SDE: `Documentation/Architecture/SDE-Implementation-Roadmap.md`, `SDE-Definition-of-Done-1.0.md`.
7. Cambios históricos: `CHANGELOG.md`; código y pruebas como evidencia, no sustituibles por narración.

En cada PR o entrega registrar: objetivo, archivos tocados, comandos efectivamente ejecutados, pruebas/hallazgos, límites de la evaluación, impactos operativos, rollback y pendientes. Si falta una prueba, declararla **no ejecutada**. Cerrar TD únicamente con evidencia congruente.

## 6. Uso con agentes compatibles

**No instalado ni validado sobre el equipo SineOS en esta documentación.** Según el README upstream, los ejemplos de invocación son:

| Host | Instalar mediante | Invocar para empezar |
|---|---|---|
| Claude Code | `./setup --host claude` | `/office-hours` |
| OpenCode | `./setup --host opencode` | `/gstack-office-hours` |
| GitHub Copilot CLI | `./setup --host copilot` | `/gstack-office-hours` |
| OpenAI Codex CLI | `./setup --host codex` | Solicitar `gstack-office-hours` |
| Cursor | `./setup --host cursor` | Solicitar `gstack-office-hours` |
| Antigravity CLI | `./setup --host agy` | `/gstack-office-hours` |

Otros comandos emplean el mismo patrón de prefijo cuando el host lo requiere (por ejemplo, `/gstack-review` en OpenCode/Copilot). Verificar el host real y la lista de skills después del setup. **ChatGPT web no es un host gstack nativo** y no adquiere slash commands por tener estas reglas.

### Instalación local: preparación sujeta a autorización

1. En la computadora Debian SineOS, verificar `git --version`, `bun --version` (Bun 1.4.2 o superior) y qué agentes están instalados.
2. Inspeccionar README, script `setup` y efectos sobre archivos de usuario, hooks, navegador y configuración global.
3. Con autorización, clonar gstack **fuera del repositorio**: `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack`.
4. Ejecutar desde `~/gstack` solo el host realmente usado, por ejemplo `./setup --host opencode` o `./setup --host copilot`; `--host auto` únicamente si se desea instalar en todos los agentes detectados.
5. Inspeccionar `./setup --status` y probar un skill de **planeación/solo lectura** antes de conceder acceso operativo.
6. Registrar versión, host, rutas y pruebas en un cambio documental posterior. La ausencia de Bun o una modificación global no aprobada detiene la instalación.

**Modo de equipo (propuesto, NO aplicado):** evaluar la modalidad `optional` antes que `required`, fijar responsables de PR y revisión, compartir estas reglas en el repo y decidir aparte si aceptar hooks/actualizaciones automáticas. Upstream documenta `./setup --team` y `bin/gstack-team-init optional` para Claude Code. No activarlos sin acuerdo del equipo y revisión de efectos globales.

## 7. Reutilización en proyectos futuros

1. Instalar gstack una sola vez por host compatible; no clonarlo dentro de cada proyecto.
2. Leer las reglas existentes del proyecto; **agregar** el bloque mínimo, nunca sobrescribirlas.
3. Sustituir rutas, stack, pruebas, riesgos y gates por los del proyecto; no copiar ciegamente los de SineOS.
4. Mantener el enlace de referencia y documentar host/versión y limitaciones reales.

### Sección mínima que se puede copiar en otro AGENTS.md / CLAUDE.md

```markdown
## gstack — método de desarrollo
Referencia: https://github.com/garrytan/gstack (MIT).
gstack se instala por separado en el agente compatible; no copiar su código al proyecto.
Flujo: Pensar (/office-hours) → Planear (/plan-eng-review) →
Construir (tras aprobar alcance) → Revisar (/review) →
Probar (/qa o /qa-only) → Lanzar (/ship) → Reflexionar (/retro).
Investigar incidentes con /investigate y revisar seguridad con /cso.
Principios ETHOS: buscar antes de construir; completar y probar la unidad
de trabajo aprobada; el usuario conserva la decisión final.
Respetar arquitectura, reglas, tests, prioridades y seguridad del proyecto.
No ejecutar acciones destructivas ni cambios globales o de producción sin permiso.
La existencia de estas instrucciones no demuestra que las skills estén instaladas.
Comprobar nombres de invocación reales (algunos hosts usan gstack-).
```

## 8. Alcance de esta adopción

Este documento y `AGENTS.md` establecen reglas de colaboración, no prueban instalación de Bun, gstack, Chromium, hooks o skills. No modifican código, contenedores, servicios, reglas de seguridad, backups ni el estado real del host. La implementación se hará en futuras tareas autorizadas, siguiendo el roadmap original.
