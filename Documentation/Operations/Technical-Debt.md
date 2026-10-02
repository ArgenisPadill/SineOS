# SineOS — Deuda técnica

Última revisión: 02-10-2026

Este documento registra únicamente deuda vigente.

## Resumen

| ID | Prioridad | Área | Pendiente |
|---|---|---|---|
| TD-006 | Media | Open WebUI | Fijar imagen por versión/digest |
| TD-007 | Media | Open WebUI | Retirar restart automático y recrear |
| TD-008 | Media | Red | Revisar nftables + Podman/netavark |
| TD-009 | Media | Ollama | Validar 11434 desde otro equipo |
| TD-010 | Media | Seguridad | Auditoría formal de AppArmor |
| TD-011 | Media | Privacidad | Determinar consumidores de Tor |
| TD-012 | Media | Miyo | Actualización CLI/AppImage |
| TD-013 | Media | Miyo | Benchmark semántico multinota |
| TD-014 | Baja | Paquetes | Revisar apt autoremove manualmente |
| TD-015 | Media | Recuperación | Procedimiento de migración |
| TD-017 | Media | Vault | Templates Incidencia/Procedimiento/ADR |
| TD-018 | Alta | Seguridad | Ejecutar validación final asistida por agente después de cerrar el hardening restante |
| TD-019 | Media | Stirling PDF | Revisar permisos de `/configs` al actualizar desde 2.14.3; la versión actual restablece archivos sensibles a 755 al arrancar |
| TD-024 | Media | Recuperación | Normalizar ownership de Uptime Kuma durante restore sobre host limpio |

## Decisiones cerradas

**Firewall:** nftables está operativo con INPUT `drop`. Ya no es deuda implementar un firewall.

**PostgreSQL/Quadlet:** la política vigente es arranque manual desde Podman Desktop y loopback `127.0.0.1:5432`. Quadlet/autostart deja de ser objetivo mientras esta decisión siga vigente.

**Open WebUI secret persistente (TD-005):** cerrado. El `WEBUI_SECRET_KEY` existente fue recuperado sin rotación, almacenado en `.env` local con permisos `600`, excluido de Git y validado mediante dos recreaciones completas del contenedor conservando el mismo secret, volumen e imagen.

**Gestión de secretos (TD-001):** cerrada. Política, inventario, permisos, Gitleaks, secret persistente de Open WebUI, auditor recurrente y procedimientos de rotación quedaron documentados y validados.

**Política general de backup (TD-002):** cerrada. SineOS adopta Restic como motor preferente para backup cifrado/versionado y Btrfs/Snapper únicamente como rollback local. La implementación se dividió en TD-003, TD-004 y TD-016; TD-003, TD-004 y TD-016 están cerradas.

**PostgreSQL backup/restore (TD-003):** cerrado. El 24-09-2026 se generó un dump lógico con `pg_dump`/ `pg_dumpall`, se validaron hashes SHA-256 y se restauró realmente en una instancia PostgreSQL 18 temporal, aislada, sin red ni puertos publicados. Se verificaron roles y estructura, se eliminó el entorno de prueba y el contenedor productivo permaneció detenido e intacto.

**Knowledge Vault backup independiente (TD-004):** cerrado. El 01-10-2026 se validó de extremo a extremo el snapshot Restic `9ec723e9` con tag `SineOsBackups-011026-0101`. El Vault restaurado coincidió con el manifiesto previo al snapshot: 70 archivos, 27 notas Markdown, 43 archivos adicionales, 33 symlinks y 99 directorios. `.obsidian` fue validado, `.opencode/node_modules` permaneció excluido y el Vault vivo no cambió durante el proceso. La evidencia quedó registrada mediante los commits `01302b9` y `ae3886f`.

**Disaster Recovery (TD-016):** cerrado el 02-10-2026. SineOS fue reconstruido en una VM Debian 13.7 limpia asumiendo pérdida del sistema original. Se recuperaron Git, Restic, Knowledge Vault, secretos necesarios, PostgreSQL, Uptime Kuma, Stirling PDF y Open WebUI. Se validaron autenticación PostgreSQL por contraseña, persistencia de los servicios, conectividad Uptime→Stirling y sincronización Git. El procedimiento probado quedó documentado en `Documentation/Recovery/Disaster-Recovery.md`. El hallazgo de ownership de Uptime Kuma se separó como TD-024.

**Salud trimestral (TD-020):** cerrada. `sineos-health-audit.sh` v1.2.3 fue validado el 24-09-2026 con 21 controles OK, 0 advertencias, 0 errores y `RESULTADO: OK`; Git quedó limpio y sincronizado con GitHub.

**Mantenimiento trimestral (TD-022):** cerrado. La aplicación GTK3, el timer, la persistencia, rollback/reinstalación y el gate GitHub no interactivo mediante GCR fueron validados el 24-09-2026. El push real del siguiente ciclo utilizará el mismo entorno GCR ya probado para operaciones remotas.

**Primer respaldo externo certificado (TD-021):** cerrado. El 24-09-2026 se creó el snapshot Restic `536d25fd` con tag `SineOsBackups-240926-2334`, se ejecutó `restic check` sin errores y se validó una restauración real. PostgreSQL, Uptime Kuma, Open WebUI y Stirling PDF fueron probados funcionalmente desde los datos restaurados; el Knowledge Vault también fue restaurado y verificado.

**Automatización del respaldo externo (TD-023):** cerrada. El flujo completo quedó integrado en SineOS Mantenimiento: creación del snapshot, `restic check`, restauración temporal verificada, validación de Git y PostgreSQL, validaciones funcionales de Uptime Kuma, Open WebUI y Stirling PDF, registro documental mediante Commit A + Commit B y sincronización con GitHub. El 25-09-2026 se validó de extremo a extremo el snapshot `ac035822` con tag `SineOsBackups-250926-2142`. La GUI ejecuta el proceso en segundo plano, muestra el estado real del destino y bloquea la creación de otro snapshot si existe un respaldo certificado pendiente de registrar.

**DNSCrypt/Proton:** DNSCrypt por perfil y el ciclo Proton VPN/DNS fueron implementados y validados mediante NetworkPrivacy.

**Servicios retirados:** KDE Connect, i2pd y redsocks fueron retirados tras comprobar que no eran necesarios.

## Detalle

### Secretos
La política formal ya existe en `Documentation/Security/Secrets-Management.md`.

Validado el 23-09-2026:

```text
~/.config/sineos                -> 700
monitoring/*.env                -> 600
PostgreSQL .env                 -> 600
Gitleaks working tree           -> 0 hallazgos
Gitleaks historial Git          -> 0 hallazgos
```

TD-001 cerrado el 23-09-2026. El auditor recurrente v1.1.0 fue validado con 12 controles OK, 0 advertencias y 0 errores; la rotación quedó documentada en `Documentation/Security/Secrets-Rotation.md`.

### Backups y recuperación
La política general está definida en `Documentation/Recovery/Backup-Policy.md`. El destino físico separado, el repositorio Restic y el flujo certificado de backup/restore están implementados y validados.

TD-003, TD-004 y TD-016 están cerradas. El Knowledge Vault cuenta con validación por manifiesto, SHA-256, estructura de directorios, symlinks sin seguimiento, `.obsidian`, exclusiones y comparación real origen/restore.

TD-016 quedó cerrado el 02-10-2026 después de una reconstrucción completa y validada sobre Debian 13 limpio. El procedimiento está documentado en `Documentation/Recovery/Disaster-Recovery.md`. TD-024 mantiene pendiente automatizar la corrección de ownership de Uptime Kuma observada durante el DR. Snapshot Btrfs no equivale a backup.

### Open WebUI
El secret persistente ya quedó validado y TD-005 está cerrado. Permanecen como deuda fijar la imagen y retirar `restart: unless-stopped` mediante recreación controlada preservando datos.

### Red y Ollama
Validar 11434 desde otro equipo y comprobar que recargar nftables no interfiera con netavark.

### AppArmor
Está activo, pero falta auditoría formal con herramientas adecuadas.

### Tor
Escucha solo en `127.0.0.1:9050`. Antes de retirarlo debe comprobarse si alguna aplicación consume ese SOCKS local.

### Paquetes
No ejecutar `apt autoremove` a ciegas. `sshfs` apareció entre candidatos y puede seguir siendo útil.

### Miyo y Vault
Formalizar actualización, continuar benchmarks y crear templates técnicos.

### Stirling PDF
La imagen estable 2.14.3 ejecuta `chmod -R 755` sobre `/configs` durante el arranque. Esto revierte permisos restrictivos aplicados a claves JWT y backups SQL. No se mantiene un parche local; se revisará una futura versión estable donde upstream ya haya corregido esta lógica.

### Validación final asistida por agente
La fase final utilizará una allowlist defensiva de `Anthropic-Cybersecurity-Skills` después de cerrar las capas tradicionales de hardening y recuperación. No debe marcarse como completada por instalar la biblioteca: requiere evaluación, evidencia, remediación individual y revalidación.

## Regla de cierre
Una deuda se cierra solo después de aplicar y validar el cambio.
