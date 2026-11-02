# SineOS — Coherencia de roadmap, issues, PR y publicación

**Corte:** 02-11-2026. Auditoría documental, sin cierre de issues ni merge. `main` continúa como baseline.

## Trazabilidad de decisiones y gates

| Prioridad / dependencia | Seguimiento | Estado conforme a documentos consultados |
| --- | --- | --- |
| Roadmap maestro y orden A→F | [#4](https://github.com/ArgenisPadill/SineOS/issues/4) | Abierto; fuente `Documentation/Operations/Project-Roadmap.md` |
| Gate Seguridad (primero) | [#2](https://github.com/ArgenisPadill/SineOS/issues/2) | Abierto. Sin PASS global; bloqueo de SDE físico |
| SDE 1.0 (segundo) | [#1](https://github.com/ArgenisPadill/SineOS/issues/1) | Planificado; implementación/certificación pendientes |
| Oracle/n8n/Minecraft (tercero) | [#5](https://github.com/ArgenisPadill/SineOS/issues/5) | Planificado, después de SDE |
| Reproducibilidad / migración | TD-015, [PR #12](https://github.com/ArgenisPadill/SineOS/pull/12) | Material preparatorio sin integración, gate de host/digests PENDING |
| SLDE (posterior a reproducibilidad) | [#3](https://github.com/ArgenisPadill/SineOS/issues/3) | Planificado, no implementado |
| Office piloto independiente y congelado | [#7](https://github.com/ArgenisPadill/SineOS/issues/7), [#8](https://github.com/ArgenisPadill/SineOS/issues/8), [#9](https://github.com/ArgenisPadill/SineOS/issues/9), [#10](https://github.com/ArgenisPadill/SineOS/issues/10) | RDP único funcional; RemoteApp experimental; recuperación y seguridad pendientes. No descongelar ni asumir integrado |
| Codex multiagente, metodología futura | [#11](https://github.com/ArgenisPadill/SineOS/issues/11) | Propuesta, sin instalación local ni autorización de ejecución |

## Pull Requests en revisión

- [PR #6](https://github.com/ArgenisPadill/SineOS/pull/6): adopción documental de metodología gstack. **Abierto; no considerar su contenido vigente en `main`**.
- [PR #12](https://github.com/ArgenisPadill/SineOS/pull/12): bootstrap/inventario/checklist/pinning pendiente. **Borrador; no declarar `bootstrap.sh` disponible en `main`**.
- Esta revisión añade orientación, SECURITY y checklists; tampoco certifica el host.

## Decisiones congeladas y conflictos a prevenir

1. El gate #2 siempre precede a implementación física de SDE. Esta revisión NO modifica la precedencia.
2. SineOS Office es un piloto operativo congelado, no certificado. Documentar el piloto no equivale a integrarlo.
3. Podman se mantiene rootless. PostgreSQL, Uptime Kuma y Stirling PDF conservan arranque manual; no introducir restart automático por documentación.
4. `Disaster-Recovery.md` registra validación histórica de PostgreSQL, Vault y Uptime Kuma. TD-024 trata específicamente automatización/ownership restaurado y permanece abierto.
5. Versiones fijadas por digest y tests reales son gates posteriores; documentación no autoriza recrear servicios en producción.
6. Antes de merge, revisar PR #6 y PR #12 por referencias, cambios de `AGENTS.md` y conflictos de contexto; aprobar cambios por separado.

## Falta de LICENSE: decisión del propietario

Un repositorio público **no** implica autorización general para reutilizar, modificar o distribuir el código. No se agregó `LICENSE` porque elegir licenciamiento tiene implicaciones legales y de propiedad intelectual.

Opciones para discutir con el propietario:
- **MIT**: licencia permisiva breve, con aviso de copyright.
- **Apache-2.0**: permisiva con cláusulas expresas sobre patentes y avisos.
- **GPL-3.0-only**: copyleft que exige condiciones para redistribución de obras derivadas.
- **Sin licencia explícita**: no hay licencia abierta para terceros; menos adecuado si se desea colaboración comunitaria.

Antes de elegir una licencia, comprobar derechos sobre aportaciones, dependencias, documentación, imágenes, scripts externos y componentes de terceros. **PENDING: decisión del propietario; no crear `LICENSE` como sustitución automática.**

## GitHub “About”

El conector disponible permite consultar el repositorio pero no actualizar su campo “About”/Topics. Propuesta breve para editar manualmente desde GitHub:

**Description:** `SineOS: entorno reproducible de sistemas, desarrollo, contenedores y recuperación sobre Debian 13 y Podman rootless.`

**Topics sugeridos:** `debian`, `podman`, `xfce`, `disaster-recovery`, `homelab`, `automation`. No publicar ubicaciones, equipos o contactos privados.

## Criterios de cierre de esta revisión

- PR revisado y checks de Markdown/rutas sin errores.
- Auditoría de privacidad e historial y license/contacto responsable resueltos por el propietario.
- Las pruebas de cada stack pasan realmente en ambiente aislado; registrar PASS/FAIL/PENDING.
- Roadmap e issues no se alteran por inferencia y Office continúa congelado.
