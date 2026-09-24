# SineOS — Deuda técnica

Última revisión: 23-09-2026

Este documento registra únicamente deuda vigente.

## Resumen

| ID | Prioridad | Área | Pendiente |
|---|---|---|---|
| TD-001 | Alta | Secretos | Formalizar gestión de secretos |
| TD-002 | Alta | Backups | Política general de backup |
| TD-003 | Alta | PostgreSQL | Backup y restauración probados |
| TD-004 | Alta | Vault | Backup independiente del Knowledge Vault |
| TD-005 | Alta | Open WebUI | Secret persistente fuera de Git |
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
| TD-016 | Alta | Recuperación | Prueba de Disaster Recovery |
| TD-017 | Media | Vault | Templates Incidencia/Procedimiento/ADR |
| TD-018 | Alta | Seguridad | Ejecutar validación final asistida por agente después de cerrar hardening y DR |
| TD-019 | Media | Stirling PDF | Revisar permisos de `/configs` al actualizar desde 2.14.3; la versión actual restablece archivos sensibles a 755 al arrancar |

## Decisiones cerradas

**Firewall:** nftables está operativo con INPUT `drop`. Ya no es deuda implementar un firewall.

**PostgreSQL/Quadlet:** la política vigente es arranque manual desde Podman Desktop y loopback `127.0.0.1:5432`. Quadlet/autostart deja de ser objetivo mientras esta decisión siga vigente.

**DNSCrypt/Proton:** DNSCrypt por perfil y el ciclo Proton VPN/DNS fueron implementados y validados mediante NetworkPrivacy.

**Servicios retirados:** KDE Connect, i2pd y redsocks fueron retirados tras comprobar que no eran necesarios.

## Detalle

### Secretos
Centralizar criterios para `.env`, URLs Push, claves y futuras credenciales. Ningún secreto real debe entrar en Git.

### Backups y recuperación
Definir frecuencia, retención, destino y pruebas. Prioridad: Knowledge Vault y PostgreSQL. Snapshot Btrfs no equivale a backup.

### Open WebUI
Fijar imagen, definir secret persistente y retirar `restart: unless-stopped` mediante recreación controlada preservando datos.

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
