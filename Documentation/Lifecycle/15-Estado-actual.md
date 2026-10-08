# 15 — Estado actual de SineOS

**Checkpoint documental:** 07-10-2026

## Estado general

SineOS se encuentra en:

```text
BASE FUNCIONAL VALIDADA
+
BACKUP / RESTORE / DR VALIDADOS
+
HARDENING DE SEGURIDAD EN PROGRESO
+
SDE 1.0 PLANIFICADO / IMPLEMENTACIÓN FÍSICA PAUSADA
```

La implementación física de SineOS Desktop Experience (SDE) no debe comenzar hasta concluir o aceptar conscientemente el bloque de seguridad pendiente.

## Componentes validados o funcionales

```text
Debian 13 / XFCE
Btrfs
Git + GitHub SSH
Podman rootless
PostgreSQL 18
Ollama
Qwen local
Open WebUI
Obsidian / Knowledge Vault
Miyo
Stirling PDF
Uptime Kuma
nftables
Proton VPN
DNSCrypt
NetworkPrivacy
SineOS · Mantenimiento
auditoría trimestral
configuración XFCE reproducible
monitoreo local
backup externo Restic
restore probado
Disaster Recovery
```

## Programas propios

```text
NetworkPrivacy
SineOS · Mantenimiento
```

Catálogo autoritativo:

`Apps/README.md`

## Automatizaciones versionadas principales

```text
Scripts/Audit/sineos-audit.sh
Scripts/Audit/sineos-health-audit.sh
Scripts/Desktop/sineos-xfce-macos.sh
Scripts/Monitoring/check-open-webui.sh
Scripts/Monitoring/check-postgresql.sh
Scripts/NetworkPrivacy/install-network-privacy.sh
Scripts/Maintenance/install-sineos-maintenance.sh
Scripts/Maintenance/run-health-audit-interactive.sh
Scripts/Security/sineos-secrets-audit.sh
Containers/stacks/postgres/Makefile
```

Catálogo autoritativo:

`Scripts/README.md`

## Recuperación validada

Están cerrados y no deben seguir listándose como huecos:

- gestión de secretos (TD-001);
- política general de backup (TD-002);
- backup/restore PostgreSQL (TD-003);
- backup independiente del Knowledge Vault (TD-004);
- secret persistente Open WebUI (TD-005);
- Disaster Recovery (TD-016);
- salud trimestral (TD-020);
- primer respaldo externo certificado (TD-021);
- SineOS · Mantenimiento (TD-022);
- automatización del respaldo externo (TD-023).

El procedimiento DR validado vive en:

`Documentation/Recovery/Disaster-Recovery.md`

El estado autoritativo del último backup vive en:

`Documentation/Recovery/Backup-Status.md`

## Deuda vigente

La fuente de verdad es:

`Documentation/Operations/Technical-Debt.md`

Pendientes principales actuales:

- TD-006: fijar imagen/digest Open WebUI;
- TD-007: retirar restart automático de Open WebUI;
- TD-008: revisar nftables + Podman/netavark;
- TD-009: validar Ollama desde otro equipo;
- TD-010: auditoría formal de AppArmor;
- TD-011: determinar consumidores de Tor;
- TD-012: actualización Miyo;
- TD-013: benchmark semántico multinota;
- TD-014: revisar `apt autoremove`;
- TD-015: procedimiento de migración;
- TD-017: templates técnicos del Vault;
- TD-018: validación final de seguridad asistida por agente;
- TD-019: permisos de Stirling PDF;
- TD-024: ownership Uptime Kuma durante restore;
- TD-025: portabilidad de `sineos-audit.sh`.

## Huecos de reproducibilidad/documentación todavía reales

1. procedimiento integral de instalación de SineOS desde Debian limpio fuera del escenario específico de DR;
2. verificación/documentación de LUKS;
3. instalación reproducible completa de Podman Desktop;
4. instalación reproducible completa de Obsidian;
5. instalación/reinstalación reproducible de Miyo;
6. unidades/timers exactos del monitoreo recurrente aún requieren formalización completa;
7. ruleset nftables operativo debe quedar versionado/saneado como artefacto reproducible;
8. inventario global de dependencias;
9. procedimiento global de actualización de SineOS;
10. troubleshooting general por capas.

## Seguridad pendiente antes de SDE físico

Orden aproximado:

```text
AppArmor
  ↓
LUKS
  ↓
inventario de puertos
  ↓
nftables / Podman / netavark
  ↓
validación LAN y exposición de Ollama
  ↓
hardening SSH si existe servidor SSH habilitado
  ↓
rotación/gestión de credenciales pendientes
  ↓
política de snapshots
  ↓
TD-024
  ↓
validación final de seguridad asistida por agente
```

No se deben ejecutar todos estos cambios de una sola vez. Cada control requiere evidencia, rollback cuando corresponda y revalidación.

## SineOS Desktop Experience

La planeación funcional y técnica inicial de SDE 1.0 está congelada en el issue maestro #1 y en `Documentation/Architecture/SDE-*.md`.

Alpha 0.1 ya tiene definidos:
- backup pre-SDE;
- SHA-256;
- verify;
- restore dry-run;
- restore reanudable;
- ownership;
- conflictos;
- uninstall seguro;
- Last Known Good;
- Modo seguro.

**Estado:** no implementar todavía sobre la laptop hasta cerrar el gate de seguridad.

## Comprobación operativa

Para comprobar el repositorio:

```bash
cd "$HOME/Workspace/SineOS"
git status
git log -1 --oneline --decorate
git ls-files | sort
```

Para comprobar el sistema:

```bash
systemctl --failed --no-pager
podman ps -a
nmcli connection show --active
sudo nft list ruleset
ss -tulpn
```

## Fuente de verdad

- estado global: este documento;
- deuda vigente: `Documentation/Operations/Technical-Debt.md`;
- seguridad: `Documentation/Security/Security-Baseline.md`;
- último health: `Documentation/Operations/Health-Status.md`;
- último backup: `Documentation/Recovery/Backup-Status.md`;
- DR: `Documentation/Recovery/Disaster-Recovery.md`;
- SDE: issue #1 + documentos `SDE-*.md`.

## Regla de actualización

Este archivo representa el estado vigente, no una cronología infinita.

Cuando una deuda se cierre o un componente cambie de estado:
1. actualizar su documento operativo;
2. actualizar Technical Debt;
3. actualizar este checkpoint si cambia el estado global;
4. actualizar CHANGELOG;
5. sincronizar con GitHub.
