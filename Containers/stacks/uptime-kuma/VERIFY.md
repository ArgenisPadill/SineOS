# Uptime Kuma — checklist de verificación

**Estado:** procedimiento propuesto; ejecución en host nuevo PENDING. TD-024 abierto.

| Paso | Inspección / prueba | Aceptación |
| --- | --- | --- |
| 1 | `podman info --format '{{.Host.Security.Rootless}}'` | `true`. |
| 2 | `podman network exists sineos-monitoring` y `podman inspect sineos-uptime-kuma --format '{{.ImageName}}'` | Red existente; imagen efectiva registrada; tag `:2` necesita pinning. |
| 3 | `podman port sineos-uptime-kuma` | Publicación en `127.0.0.1:3001` únicamente. |
| 4 | `curl --noproxy '*' --connect-timeout 3 --max-time 10 -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3001/` | HTTP 2xx/3xx cuando se inicia manualmente. |
| 5 | En clon aislado del volumen, comprobar arranque de Embedded MariaDB y monitores restaurados. | Sin fallos de `aria_log_control` ni `ibdata1`, estado de monitores persistente. |
| 6 | Si falla el ownership del **clon** restaurado: `podman unshare chown -R 1000:1000 "<VOLUMEN_DE_PRUEBA>"` y repetir la prueba. | PASS de recuperación tras normalizar permisos; pendiente integrar el paso con seguridad en el flujo automático TD-024. |

**Nunca** aplicar recursivamente `chown` a un volumen productivo sin parada, respaldo y autorización; el ejemplo está restringido al clon de recuperación.

**Rollback:** mantener snapshot y host origen; no reemplazar volumen productivo. Las URLs Push de `~/.config/sineos/monitoring/` son secretos y no se imprimen.
