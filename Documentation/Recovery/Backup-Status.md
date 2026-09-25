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


## Restic instalado

Validado el 24-09-2026:

```text
Binario: /usr/bin/restic
Versión: 0.18.0
Paquete Debian: 0.18.0-1+b4
Repositorio Restic: NO INICIALIZADO
Backup: DESHABILITADO
```

La instalación del motor no equivale a un respaldo válido. Falta definir la credencial de recuperación, inicializar el repositorio y ejecutar backup + check + restore.


## Credencial Restic local

Validado el 24-09-2026:

```text
Ruta local: ~/.config/sineos/restic-password
Permisos: 600
Propietario: usuario SineOS
Contenido expuesto: no
Repositorio Restic: todavía no inicializado
```

La credencial no se versiona en Git ni se almacena en el disco externo de backup.

Antes de ejecutar `restic init` debe existir una copia de recuperación independiente de la laptop y del disco `InfoDGRC`.


## Repositorio Restic inicializado

Validado el 24-09-2026:

```text
Repositorio: /media/argenis/InfoDGRC/SineOsBackups
ID: a1f88f2abd…
Formato: versión 2
Compresión: auto
Snapshots: 0
restic check: OK
Errores: 0
Backup activo: no
```

La inicialización y el `restic check` validan el repositorio vacío, pero todavía no constituyen un respaldo de SineOS.


## PostgreSQL — dump lógico preliminar

Validado el 24-09-2026:

```text
PostgreSQL: 18.6
Estado inicial del contenedor: detenido
Base postgres: ~7521 kB
Base sineos: ~7710 kB
Tablas de usuario en sineos: 0
Secuencias de usuario en sineos: 0
Vistas de usuario en sineos: 0
Tablas de usuario en postgres: 0
database.dump: formato custom, legible por pg_restore
globals.sql: generado
Estado final del contenedor: detenido
```

El tamaño reducido del dump es coherente con una base `sineos` sin objetos de usuario. TD-003 permanece abierto hasta ejecutar una restauración real en un PostgreSQL temporal.


## PostgreSQL — restauración real validada

Validado el 24-09-2026:

```text
Dump lógico: OK
globals.sql: OK
SHA-256: OK
Imagen de restore: docker.io/library/postgres:18
Contenedor temporal: aislado, sin red ni puertos
Inicialización completa: OK
Servidor definitivo estable: OK
Roles no-sistema restaurados: 1
database.dump restaurado: OK
Tablas de usuario: 0
Secuencias de usuario: 0
Vistas de usuario: 0
Entorno temporal eliminado: OK
PostgreSQL productivo final: Running=false / Status=exited
Residuos temporales: ninguno
```

TD-003 queda cerrado. El dump validado queda disponible como origen para el primer snapshot certificado de TD-021.
