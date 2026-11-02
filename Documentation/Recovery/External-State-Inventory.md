# SineOS — Inventario del estado fuera de Git

**Estado:** inventario documental preparado el 02-11-2026; rutas y respaldo actual deben verificarse en el host antes de migrar. No contiene secretos ni datos privados.

La ruta versionada `${SINEOS_REPO}` no equivale a los datos privados ni al Vault de Obsidian. Nunca asumir que `git clone` restaura el sistema completo.

| Ruta o identificador | Contenido / estado | Protección y recuperación |
| --- | --- | --- |
| `${SINEOS_REPO}` (ejemplo habitual `~/Workspace/SineOS`) | Código, Compose y documentación versionados; también directorios locales ignorados | Clonar Git; respaldar **por separado** los directorios ignorados. No asumir que todo el árbol es Git. |
| `${SINEOS_VAULT}` | Vault de Obsidian; notas, adjuntos, plantillas y configuración `.obsidian` | Restic cifrado a disco externo; restaurar de forma temporal y comparar manifiesto, hash, enlaces y estructura. |
| `~/.config/sineos/monitoring/` | Archivos privados de Uptime Kuma Push (ej. `open-webui.env`, `postgresql.env`) | Restic cifrado; permisos de directorio 700 y archivos 600; no imprimir ni publicar URLs Push. |
| `~/.config/sineos/` | Configuración operativa privada, controles y posibles secretos | Restic cifrado según Backup-Policy; la contraseña del repositorio Restic se conserva **fuera** del propio backup. |
| `${SINEOS_REPO}/Containers/stacks/*/.env` | Configuración local y secretos de stacks, ignorados por Git | Restic cifrado siguiendo el backup certificado; recrear desde `.env.example` solo si no existe una copia íntegra. Permisos 600. |
| `${SINEOS_REPO}/Containers/volumes/open-webui/data/` | SQLite, estado y preferencias de Open WebUI | Restic cifrado; excluir `cache/`, que puede volver a descargarse. |
| `${SINEOS_REPO}/Containers/volumes/uptime-kuma/data/` | Configuración, historial y MariaDB embebida de Uptime Kuma | Restic cifrado; al restaurar, revisar ownership de UID/GID 1000:1000 mediante `podman unshare`, solo en volumen de recuperación. |
| `${SINEOS_REPO}/Containers/volumes/stirling-pdf/` | Configuración, datos, claves generadas y archivos de Stirling PDF | Restic cifrado con exclusiones certificadas; revisar permisos del subárbol `configs` después de restaurar. |
| `${SINEOS_REPO}/Containers/volumes/postgres/data/` | Directorio PostgreSQL **vivo** | Excluido de Restic; NO recuperarlo mediante copia de archivos en caliente. Usar dump lógico certificado. |
| `~/.local/state/sineos/backup/staging/postgresql-*/` | Staging de dump lógico PostgreSQL, `globals.sql`, `database.dump` y hashes | Incluir el staging consistente en snapshot Restic certificado; probar restore de roles y base en entorno aislado. |
| `${SINEOS_BACKUP_ROOT}` (disco externo `SineOsBackups`) | Repositorio Restic cifrado y snapshots de recuperación | Verificar UUID, serial y repository ID, `restic check` y restauración de prueba; no ubicar en el mismo disco principal. |
| `SINEOS_VAULT` y `SINEOS_REPO` | Variables de entorno que apuntan a ubicaciones locales | Reestablecer sus valores **en el host**, sin imponer rutas privadas en documentación pública; comprobar con `test -d`. |
| Configuración de `ollama.service` y modelos locales | Runtime Ollama del host, override systemd y modelos descargables | Versionar el procedimiento; registrar/reaplicar overrides seguros de forma controlada. Modelos se pueden volver a descargar; no asumir que el bootstrap migra modelos. |
| `~/Workspace/SineOS-Office/` si existe | Piloto Office independiente (WinApps/QEMU/VM, `storage`, `.env`) | **Fuera del alcance** del DR certificado general. Respaldo y recuperación específicos pendientes; no mover ni tocar en esta migración. |

## Precisión sobre el motor de backup

El motor vigente `Apps/Maintenance/backup_engine.py` utiliza explícitamente `~/Obsidian/SineOS` como fuente del Vault y `~/.config/sineos` como fuente de configuración privada. **PENDING:** comprobar en el equipo que `${SINEOS_VAULT}` coincide con esa ubicación y, si no, corregir el motor mediante cambio revisado antes de certificar la copia.

La política de backup oficial es trimestral; antes de una migración se exige **copia extraordinaria** con validación del repositorio y restauración temporal. El RPO real puede ser de hasta tres meses sin copias intermedias. La evidencia histórica de TD-016 no acredita por sí sola el respaldo más reciente.

### Comprobación no destructiva en la máquina origen

```bash
test -n "${SINEOS_REPO:-}" && test -d "$SINEOS_REPO" && echo "Repositorio: OK"
test -n "${SINEOS_VAULT:-}" && test -d "$SINEOS_VAULT" && echo "Vault: OK"
test -d "$HOME/.config/sineos/monitoring" && echo "Monitoring: OK"
podman ps --all --format '{{.Names}}: {{.Status}}'
```

No adjuntar resultados de `env`, `cat *.env`, `restic cat`, ni dumps a GitHub. Documentar solo PASS/FAIL/PENDING sin valores sensibles.

**Referencias:** `Documentation/Recovery/Backup-Policy.md`, `Documentation/Recovery/Disaster-Recovery.md`, `Documentation/Security/Secrets-Management.md` y `Apps/Maintenance/backup_engine.py`.
