# Open WebUI — checklist de verificación

**Estado:** procedimiento propuesto; ejecución en host nuevo PENDING.

| Paso | Inspección / prueba | Aceptación |
| --- | --- | --- |
| 1 | `podman info --format '{{.Host.Security.Rootless}}'` | `true`. |
| 2 | `podman inspect sineos-open-webui --format '{{.ImageName}}'` y `podman port sineos-open-webui` | Imagen registrada y bind local `127.0.0.1:3000`. El tag `main` requiere pinning. |
| 3 | `curl --noproxy '*' --connect-timeout 3 --max-time 10 -fsS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3000/health` | HTTP 200 cuando el servicio está iniciado. |
| 4 | `test -s Containers/stacks/open-webui/.env && stat -c '%a' Containers/stacks/open-webui/.env` (desde raíz del repo) | Archivo existente y permisos 600; no mostrar contenido. |
| 5 | Verificar acceso a Ollama desde la interfaz y revisión de inicio sin reinicios continuos. | API funcional, sin bucles de reinicio; observar si necesita recalcular embeddings. |
| 6 | En **restore aislado**, comprobar integridad SQLite y que se mantiene el mismo `WEBUI_SECRET_KEY` mediante test funcional sin imprimir el valor. | Datos, usuarios y estado recuperados; `integrity_check: ok`; secretos nunca publicados. |

**Limitaciones:** `curl` confirma disponibilidad, no seguridad de cuenta ni consistencia de SQLite. El compose vigente tiene `restart: unless-stopped`; TD-006 y TD-007 no se cierran por estas pruebas.

**Rollback:** mantener copia restaurable y versión anterior compatible; no recrear producción antes de aprobar digest, datos y secretos.
