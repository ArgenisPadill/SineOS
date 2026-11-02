# SineOS — Verificación de servicios después de instalación o recuperación

**Estado:** checklists preparadas, sin nueva ejecución sobre el host (PENDING). **No sustituyen** las pruebas históricas de TD-016.

## Política

- Los cuatro stacks actuales tienen su propio archivo `VERIFY.md`; comprueban disponibilidad y señalan pruebas de estado persistente que requieren un entorno de restauración.
- Los servicios que se inician manualmente deben estar iniciados **por decisión del operador** antes de ejecutar su checklist. Un servicio parado deliberadamente no es evidencia de avería.
- Los comandos son orientativos y de solo lectura, salvo las **pruebas de restauración**: nunca realizar estas últimas sobre volúmenes productivos.
- No imprimir `.env`, contraseñas, URLs Push, tokens, datos de PostgreSQL, ficheros del Vault ni logs privados en GitHub.
- Comprobar bind a loopback, rootless, versión efectiva, respuesta de servicio y consistencia de estado **por separado**; HTTP 200 no demuestra persistencia.
- Cada validación debe registrar fecha, host **saneado**, commit, versión/digest de imagen, resultado PASS/FAIL/PENDING, evidencia local y acción de rollback.

| Componente | Guía | Criterios principales |
| --- | --- | --- |
| PostgreSQL | [VERIFY.md](../../Containers/stacks/postgres/VERIFY.md) | pg_isready, bind local, dump lógico y autenticación externa |
| Open WebUI | [VERIFY.md](../../Containers/stacks/open-webui/VERIFY.md) | /health, secreto persistente, SQLite y Ollama |
| Uptime Kuma | [VERIFY.md](../../Containers/stacks/uptime-kuma/VERIFY.md) | HTTP, red de monitoreo y restore MariaDB/ownership |
| Stirling PDF | [VERIFY.md](../../Containers/stacks/stirling-pdf/VERIFY.md) | HTTP, red compartida y permisos de /configs |

## Gate final

No marcar una migración como certificada hasta completar [Disaster Recovery](Disaster-Recovery.md), restaurar el Vault en ubicación temporal comprobando su manifiesto, realizar las pruebas por stack y resolver o **aceptar formalmente** las deudas de seguridad aplicables. `TD-024` permanece abierto por la automatización de ownership de Uptime Kuma; los antecedentes de Vault y PostgreSQL están documentados como validados, no como pendientes históricos.

**Propuesta de acta:** `Componente | commit | imagen efectiva | prueba | resultado | evidencia privada | riesgo | rollback`. No subir el acta con datos sensibles.

Relacionados: [Backup-Policy](Backup-Policy.md), [Technical-Debt](../Operations/Technical-Debt.md) y [PR #12 (inventario y migración aún fuera de main)](https://github.com/ArgenisPadill/SineOS/pull/12).
