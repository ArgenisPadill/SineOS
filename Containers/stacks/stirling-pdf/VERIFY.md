# Stirling PDF — checklist de verificación

**Estado:** procedimiento propuesto; ejecución en host nuevo PENDING.

| Paso | Inspección / prueba | Aceptación |
| --- | --- | --- |
| 1 | `podman info --format '{{.Host.Security.Rootless}}'` | `true`. |
| 2 | `podman inspect sineos-stirling-pdf --format '{{.ImageName}}'` | Versión efectiva registrada; `2.14.3-fat` es etiqueta de versión, no pin inmutable por digest. |
| 3 | `podman port sineos-stirling-pdf` y `podman network exists sineos-monitoring` | `127.0.0.1:8080` y red compartida presente. |
| 4 | `curl --noproxy '*' --connect-timeout 3 --max-time 10 -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/` | HTTP 200 con servicio iniciado. |
| 5 | Desde el monitor interno de Uptime Kuma comprobar `http://sineos-stirling-pdf:8080`. | HTTP 200 sin exponer servicio a LAN. |
| 6 | En copia restaurada, comprobar persistencia y permisos de `configs/backup/keys/`, sin imprimir las claves. | Archivos recuperados. **Riesgo TD-019:** entrypoint 2.14.3 ajusta `/configs` recursivamente a 755; no afirmar hardening PASS. |

**Rollback:** no sustituir imagen ni copiar permisos desde host sin prueba previa sobre respaldo; conservar volumen original e imagen compatible.
