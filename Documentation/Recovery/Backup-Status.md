# SineOS — Estado de respaldo externo

Este archivo es actualizado únicamente por el flujo de respaldo validado.

## Último respaldo validado

```text
Estado: PENDIENTE DE PRIMER RESPALDO EXTERNO VALIDADO
Fecha: —
Tag: —
Commit del evento: —
Sincronización GitHub: PENDIENTE
```

## Regla de validación

Un respaldo solo puede registrarse aquí después de:

1. crear el snapshot Restic en el disco externo;
2. ejecutar la comprobación de integridad;
3. restaurar el snapshot a una ubicación temporal;
4. validar el contenido restaurado;
5. registrar el evento en Git;
6. sincronizar la evidencia con GitHub y comprobar `HEAD local = origin/main = main remoto`.

La bitácora histórica vive en `Documentation/Recovery/Backup-Log/`.


## Hash de sincronización

El hash del commit final de bitácora/sincronización no se escribe dentro del mismo commit, porque sería autorreferencial.

La aplicación local puede guardar ese hash como `sync_commit` después del push. En GitHub, la evidencia de cierre es que:

```text
HEAD local = origin/main = main remoto
```

`Backup-Status.md` conserva el commit del evento y el estado de sincronización, no un hash autorreferencial del commit que lo contiene.


## Destino externo preparado

Validado el 24-09-2026:

```text
Montaje: /media/argenis/InfoDGRC
Partición: /dev/sdc2
Disco físico: /dev/sdc
Filesystem: ntfs3
UUID: A2B411E1B411B92D
Ruta SineOS: /media/argenis/InfoDGRC/SineOsBackups
Espacio libre aproximado: 333G
Prueba crear/leer/renombrar/borrar: OK
Disco distinto de /dev/sda: OK
SINEOS_BACKUP_ENABLED=0
Restic: todavía no instalado
```

La preparación del destino no equivale a un backup validado. El repositorio Restic aún no existe.
