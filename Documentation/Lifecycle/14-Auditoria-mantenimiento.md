# 14 — Auditoría y mantenimiento

**Estado:** AUDITOR VALIDADO / PORTABILIDAD PENDIENTE

## Auditor de SineOS

Archivo:

```text
Scripts/Audit/sineos-audit.sh
```

Está diseñado como herramienta de diagnóstico de solo lectura.

## Ejecutar

```bash
cd "$HOME/Workspace/SineOS"
bash Scripts/Audit/sineos-audit.sh
```

## Qué revisa

- sistema operativo y kernel;
- hardware y almacenamiento;
- Btrfs, memoria y swap;
- APT;
- systemd y journal;
- red;
- seguridad básica;
- Git y SSH;
- Podman;
- contenedores SineOS;
- PostgreSQL;
- XFCE, audio e input;
- SMART;
- procesos y entorno.

## Reportes

Los reportes locales están excluidos de Git.

## Deuda detectada

El auditor todavía contiene referencias históricas rígidas a `$HOME/Workspace/SineOS`. Debe migrarse a detección dinámica de la raíz del repositorio antes de declararlo portable.

## Comprobación rápida después de cambios

```bash
git -C "$HOME/Workspace/SineOS" status
systemctl --failed --no-pager
journalctl -p err -b --no-pager
podman ps -a
ss -tulpn
```

## Actualizaciones

Antes de una actualización importante registrar estado:

```bash
git -C "$HOME/Workspace/SineOS" status
podman ps -a
systemctl --failed --no-pager
```

Después de actualizar revisar al menos servicios, puertos, permisos, contenedores, logs, firewall e integraciones.

## Regla de cambios

```text
diagnosticar
documentar estado
cambiar una capa
validar
documentar resultado
```

No realizar múltiples cambios de infraestructura simultáneamente cuando eso impida identificar la causa de una falla.