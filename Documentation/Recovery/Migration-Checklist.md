# SineOS — Checklist de migración / reconstrucción

**Estado:** PROPUESTO; basado en DR TD-016 validado el 02-10-2026, pero esta checklist y el bootstrap nuevo **no** han sido certificados en host limpio. No altera el roadmap ni desbloquea Seguridad/SDE.

**Objetivo:** migrar de un equipo a otro preservando datos, secretos, PostgreSQL, redes, servicios y escritorio. **No** desplegar automáticamente contenedores ni cambiar configuraciones sensibles.

| Orden | Paso obligatorio | Prueba de éxito / criterio de avance |
| --- | --- | --- |
| 0 | Registrar baseline de origen, versión Git, estado de servicios, imágenes efectivas y destinos de almacenamiento. Consultar \`External-State-Inventory.md\`. | Inventario completo; diferencias, deudas y elementos sin backup en **PENDING** explícito. |
| 1 | En origen, crear respaldo extraordinario mediante SineOS · Mantenimiento (Git + Restic + dump lógico PostgreSQL). Confirmar identidad de disco y credenciales independientes. | Snapshot nuevo listado; \`restic check\` satisfactorio; restauración temporal y comparaciones certificadas. No confundir snapshot de octubre con copia actual. |
| 2 | Reservar equipo destino compatible (Debian 13 amd64), disco y red; mantener origen intacto. | Debian 13 confirmado; almacenamiento destino suficiente; origen recuperable. |
| 3 | Instalar Git, clonar repo y verificar commit objetivo. | \`git status -sb\` limpio y \`git rev-parse HEAD\` coincide con revisión aprobada. |
| 4 | Revisar \`bash Scripts/Bootstrap/bootstrap.sh --dry-run\` y ejecutar \`--apply\` **solo tras aprobación**. | \`git --version\`, \`podman --version\`, \`podman-compose --version\`, \`ollama --version\` (si se instaló) y paquetes XFCE presentes. La prueba integral del script sigue PENDING hasta ejecutarse en destino. |
| 5 | Recuperar credenciales Restic de gestor independiente; montar disco autorizado y comprobar identidad. | UUID/serial/repository ID coinciden; \`restic snapshots\` y \`restic check\` pasan, sin divulgar secretos. |
| 6 | Restaurar el snapshot certificado en una **ruta temporal** e inspeccionar manifiesto. Restablecer \`SINEOS_REPO\` y \`SINEOS_VAULT\` de acuerdo con rutas reales. | Vault íntegro, \`.obsidian\` presente, hashes/comparaciones consistentes y rutas comprobadas con \`test -d\`. |
| 7 | Restaurar configuración privada, \`.env\` y volúmenes permitidos; permisos restrictivos (700/600); mantener PG vivo excluido. | Inventario sin faltantes críticos; \`git status --ignored\` indica los secretos como ignorados, no versionados; sin impresiones de valores. |
| 8 | Crear la red Podman \`sineos-monitoring\` si no existe. Fijar digests de imágenes **verificados** según \`Image-Pinning.md\`, conservando versión compatible con respaldo. | \`podman network exists sineos-monitoring\` y referencia de imagen por digest verificada; **bloquear recreación** si falta compatibilidad. |
| 9 | Recuperar PostgreSQL desde \`globals.sql\` y \`database.dump\` certificados, nunca copiando el datadir vivo. Ajustar ownership 999:999 donde proceda. | \`pg_isready\` OK, roles y base presentes; autenticación **externa** con contraseña correcta aceptada e incorrecta rechazada. |
| 10 | Recuperar Uptime Kuma; corregir ownership 1000:1000 si es necesario. | HTTP 2xx/3xx; estado de MariaDB embebida y monitores persistente; sin reinicios. |
| 11 | Recuperar Stirling PDF y su estado persistente. | HTTP 200 local y monitor interno desde Uptime Kuma OK; revisar permisos de claves y configuración. |
| 12 | Recuperar Open WebUI con su secreto y SQLite, usando imagen compatible. | HTTP 200, \`integrity_check\` SQLite OK, sin bucles de reinicio; Ollama accesible desde el contenedor. |
| 13 | Aplicar XFCE mediante el instalador de escritorio versionado, **previo respaldo** y autorización para cambiar inicio de sesión. | LightDM activo, sesión XFCE X11, dos paneles, tema/iconos y layout validados después del primer login. |
| 14 | Revisar Firewall, AppArmor, NNP de Ollama y seguridad rootless; no copiar indiscriminadamente reglas antiguas de red. | Servicios solo en interfaces autorizadas; \`podman info\` rootless, reglas nftables y consumidores de Ollama comprobados. Las deudas abiertas no pasan a PASS. |
| 15 | Validación final end-to-end, almacenamiento, red, backups, restauración, Git y usuario final. | **PASS final** solo si todos los gates anteriores son PASS; registrar evidencia saneada. Si falla un gate: **STOP**, recuperar último estado funcional. |

## Recuperación / rollback

Antes de cada recreación, conservar backup validado, digests/IDs efectivos, estado del equipo origen y snapshot Restic. Un fallo no autoriza borrar volúmenes ni reemplazar \`.env\`. La reversión puede consistir en **no conmutar** al nuevo equipo y volver a operar sobre el origen. Para software del destino, volver al commit o imagen anterior solo después de verificar compatibilidad del estado persistente.

## Límites

- El bootstrap instala paquetes y Ollama opcionalmente; no clona Vault ni importa credenciales.
- \`--apply\` modifica APT y puede instalar un servicio Ollama; requiere revisión y autorización.
- La fase de **pinning real por digest** necesita evidencia de las imágenes actuales del equipo origen. Hasta entonces permanece **PENDING**.
- La migración del piloto Office congelado no se incluye.
- El procedimiento completo de recuperación previamente validado sigue siendo \`Disaster-Recovery.md\`; esta checklist no reemplaza su evidencia.

**Documentos asociados:** [Inventario](External-State-Inventory.md) · [Versionado de imágenes](Image-Pinning.md) · [Disaster Recovery](Disaster-Recovery.md).
