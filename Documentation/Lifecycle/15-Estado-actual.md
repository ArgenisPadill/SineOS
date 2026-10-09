# 15 — Estado actual de SineOS

**Checkpoint documental:** 09-10-2026

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
+
ORACLE + n8n (LOCAL / EXTERNO) + MINECRAFT PLANIFICADO / NO IMPLEMENTADO
+
SLDE (16 MÓDULOS) PLANIFICADO / NO IMPLEMENTADO
```

El orden obligatorio actualizado el 09-10-2026 es: **terminar seguridad → implementar y certificar SDE 1.0 → plan Oracle Cloud/n8n/Minecraft → resto de reproducibilidad y SLDE**. Las tareas críticas requeridas por Seguridad o SDE conservan prioridad. La implementación física de SDE no debe comenzar hasta concluir y verificar el gate de seguridad, con cualquier riesgo residual expresamente aceptado.

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

## Priorización de proyectos y nuevas iniciativas (08-10-2026; actualizada 09-10-2026)

El seguimiento general y dependencias se encuentran en [Project-Roadmap](../Operations/Project-Roadmap.md) y en [issue #4](https://github.com/ArgenisPadill/SineOS/issues/4).

1. **Seguridad — EN CURSO / PRIMERO:** [issue #2](https://github.com/ArgenisPadill/SineOS/issues/2). Incluye controles físicos pendientes, TD-008/009/010/011/018/024 y evaluación de riesgos de TD-006/007/019.
2. **SDE — PLANEACIÓN TERMINADA / IMPLEMENTACIÓN NO INICIADA:** [issue #1](https://github.com/ArgenisPadill/SineOS/issues/1). Sólo comenzar Alpha 0.1 después del gate de seguridad; respetar la Definition of Done y la certificación física.
3. **Oracle Cloud + n8n + Minecraft — PLANIFICADO / NO IMPLEMENTADO / POST-SDE:** [issue #5](https://github.com/ArgenisPadill/SineOS/issues/5) y [plan de arquitectura](../Architecture/Oracle-Cloud-n8n-Minecraft-Planning.md). Dos instancias independientes (local y externa), Minecraft opcional aislado. Disponibilidad externa 24/7 deseada pero no garantizada; VM de OCI sin verificar, ningún recurso modificado.
4. **Reproducibilidad y deuda operativa — PENDIENTE / DESPUÉS DE ORACLE:** instalación integral, dependencias, actualizaciones, migración, portabilidad y TD-012/013/014/015/017/025, salvo que una se requiera antes por seguridad o SDE.
5. **SLDE — PLANIFICADO / NO IMPLEMENTADO:** [issue #3](https://github.com/ArgenisPadill/SineOS/issues/3) y [SLDE-Planning](../Architecture/SLDE-Planning.md). Catálogo de 16 módulos opcionales, sin instalar.
6. **Despliegue gradual SLDE — PENDIENTE:** herramientas ligeras, servicios opcionales, laboratorios aislados y finalmente cargas intensivas/remotas.

Los 15 registros de deuda técnica siguen vigentes en `Technical-Debt.md`; los planes SDE/SLDE no se contabilizan como deuda nueva ni como instalaciones completadas.

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
- orden general y trabajo futuro: `Documentation/Operations/Project-Roadmap.md` + issue #4.
- Oracle Cloud/n8n/Minecraft, sólo planificación: `Documentation/Architecture/Oracle-Cloud-n8n-Minecraft-Planning.md` + issue #5.
- SLDE: `Documentation/Architecture/SLDE-Planning.md` + issue #3.

## Regla de actualización

Este archivo representa el estado vigente, no una cronología infinita.

Cuando una deuda se cierre o un componente cambie de estado:
1. actualizar su documento operativo;
2. actualizar Technical Debt;
3. actualizar este checkpoint si cambia el estado global;
4. actualizar CHANGELOG;
5. sincronizar con GitHub.
