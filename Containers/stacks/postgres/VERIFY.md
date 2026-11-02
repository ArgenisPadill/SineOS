# PostgreSQL 18 — checklist de verificación

**Estado:** procedimiento propuesto; ejecución en host nuevo PENDING. No iniciar automáticamente ni modificar el volumen productivo.

| Paso | Inspección / prueba | Aceptación |
| --- | --- | --- |
| 1 | `podman info --format '{{.Host.Security.Rootless}}'` | `true`. |
| 2 | `podman inspect sineos-postgres --format '{{.ImageName}}'` | Referencia de imagen registrada y compatible con backup. `postgres:18` sigue siendo móvil sin digest certificado. |
| 3 | `podman port sineos-postgres` | Solo publicación de `127.0.0.1:5432` (o puerto local configurado y aprobado). |
| 4 | `podman exec sineos-postgres pg_isready -U sineos -d sineos` | `accepting connections`. No verifica la contraseña. |
| 5 | Desde cliente externo al contenedor, probar contraseña válida e inválida por medio seguro, **sin pasar secretos en argumentos ni guardarlos en evidencias públicas**. | Válida aceptada, inválida rechazada. Evitar que una regla local `trust` dé falso PASS. |
| 6 | Restaurar `globals.sql` y `database.dump` del staging certificado en contenedor **aislado y temporal**. | Integridad SHA-256, roles, estructura, datos esperados y prueba de conexión. No usar datadir vivo como copia de seguridad. |
| 7 | Detener la instancia de prueba; confirmar que el contenedor productivo conserva su estado. | Producción intacta; evidencia guardada fuera de Git. |

**Rollback:** no alterar imagen o volumen productivo hasta validar backup/restauración. Ante fallo, no migrar tráfico, conservar equipo origen y revalidar dump. Referencias: `Documentation/Recovery/Disaster-Recovery.md`, `Documentation/Recovery/Backup-Policy.md` y TD-003.
