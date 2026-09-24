# SineOS — Estado de respaldo externo

Este archivo es actualizado únicamente por el flujo de respaldo validado.

## Último respaldo validado

```text
Estado: PENDIENTE DE PRIMER RESPALDO EXTERNO VALIDADO
Fecha: —
Tag: —
Commit del evento: —
Commit de sincronización: —
```

## Regla de validación

Un respaldo solo puede registrarse aquí después de:

1. crear el snapshot Restic en el disco externo;
2. ejecutar la comprobación de integridad;
3. restaurar el snapshot a una ubicación temporal;
4. validar el contenido restaurado;
5. registrar el evento en Git;
6. sincronizar la evidencia con GitHub.

La bitácora histórica vive en `Documentation/Recovery/Backup-Log/`.
