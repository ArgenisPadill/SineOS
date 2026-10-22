---
name: sineos-systematic-debugging
description: Investigar errores, congelamientos o fallas de SineOS con reproducción y búsqueda de causa raíz antes de proponer arreglos; usar para bugs de Debian, Podman, XFCE, scripts, base de datos o integraciones, manteniendo el host intacto por defecto.
---

# SineOS — Depuración basada en causa raíz

**Disparador:** errores, fallas intermitentes, servicios que no inician, regresiones o soluciones previas inefectivas.

**No activar:** implementación de una función nueva sin bug o autorización genérica para 'limpiar' el sistema.

Respeta `AGENTS.md` y el [estándar general](../../../Documentation/Architecture/Engineering-Delivery-Standard.md).

1. Registrar síntoma exacto, fecha/contexto, resultado esperado vs. observado, versión/entorno y alcance. Diferenciar usuario, logs, inferencias y suposiciones.
2. Preparar la **reproducción más pequeña** posible y las observaciones de solo lectura relevantes, sin cambiar credenciales, servicios, políticas, VM ni datos.
3. Formular hipótesis contrastables y solicitar evidencia que pueda refutarlas. Revisar cambios recientes y dependencias; no encadenar parches especulativos.
4. Identificar causa raíz o declarar honestamente **NO CONCLUYENTE**. No fijar falsos positivos.
5. Proponer un cambio mínimo y único, con preflight, prueba negativa/positiva, regresión y recuperación proporcionada al riesgo; **esperar autorización de ejecución** si altera el host.
6. Solo si el usuario autorizó implementar y está protegido el baseline, probar cambio y verificar salida efectiva. Detener ante regresión.
7. Informar resultado, evidencias, cambios realmente ejecutados, rollback, problemas no resueltos y continuidad.

**Nunca:** `podman down -v`, matar procesos globalmente, borrar respaldos, editar reglas nftables con salida no verificada, cambiar configuración de RDP/Office congelado, revelar secretos o afirmar que un fallo se corrigió solo por escribir una propuesta.

**Referencia externa, no instalada:** [obra/superpowers — systematic-debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md).
