---
name: sineos-verify-delivery
description: Verificar antes de declarar completada una tarea, commit, corrección, release o issue de SineOS; reunir pruebas reales, regresiones, evidencias y capacidad de rollback, separando PASS, FAIL y PENDING sin inventar certificación.
---

# SineOS — Aceptación con evidencia

**Disparador:** solicitud de revisar un diff, verificar resultado de Codex, cerrar issue, declarar una función estable, preparar release o confirmar que un arreglo funciona.

Lee `AGENTS.md`, [norma transversal](../../../Documentation/Architecture/Engineering-Delivery-Standard.md), criterios propios del subsistema y documentación/issue relacionados.

## Procedimiento

1. Especifica **qué afirmación exacta** necesita prueba: 'archivo existe', 'servicio arranca', 'interfaz usable', 'restore funciona' y 'certificado' son niveles distintos.
2. Identifica la evidencia fresca disponible: comandos ejecutados con salida/código, hashes, tests, capturas verificadas, revisión manual del usuario y documentación. **No vuelvas a ejecutar pruebas destructivas por obtener evidencia.**
3. Comprueba el efecto sobre funciones existentes, permisos, dependencias y privacidad; delimita lo que no pudo verificarse.
4. Verifica que el rollback requerido fue ensayado o declara expresamente su límite; un hash no demuestra recuperación funcional integral.
5. Evalúa cada criterio con **PASS / FAIL / PENDING / NOT APPLICABLE**, señalando origen y limitaciones. **No cierres issues ni publiques cambios solo por disponer de documentación.**
6. Presenta informe conciso para aprobación. Si falta acceso al host, di que no se pudo verificar el comportamiento físico.

**Formato sugerido:**

| Criterio | Estado | Evidencia | Riesgo / siguiente paso |
| --- | --- | --- | --- |
| Ejemplo | PENDING | Sin ejecución en host | Solicitar prueba real |

**Fuentes externas:** [Verification Before Completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md), [Test Gap Audit](https://github.com/github/awesome-copilot/blob/main/skills/test-gap-audit/SKILL.md). Skill propia de SineOS, no copia de dependencias externas.
