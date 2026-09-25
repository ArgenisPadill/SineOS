# SineOS — Estado de respaldo externo

Este archivo es actualizado únicamente por el flujo de respaldo validado.

## Último respaldo validado

```text
Estado: VALIDADO
Fecha: 24-09-2026
Tag: SineOsBackups-240926-2334
Snapshot Restic: 536d25fd
Commit del evento: daeb26661a6192512f48c4f6688aa6b0166904f6
Sincronización GitHub: VALIDADA
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


## Incidente NTFS durante TD-021

El 24-09-2026 el disco externo sufrió una desconexión USB mientras NTFS tenía escrituras pendientes.

Evidencia observada:

```text
USB disconnect
Buffer I/O error / lost sync page write
ntfs_set_state failed
ntfs3_write_inode failed
volumen marcado dirty
$MFTMirr no coincide con $MFT
```

Diagnóstico físico posterior del NVMe:

```text
SMART overall-health: PASSED
Critical Warning: 0x00
Media and Data Integrity Errors: 0
Error Information Log Entries: 0
Temperature: 35 C
Percentage Used: 4%
```

El repositorio Restic queda temporalmente fuera de uso hasta reparar y volver a montar el filesystem NTFS de forma normal. Después de la reparación se debe ejecutar nuevamente `restic check` antes de continuar con el primer snapshot certificado.


## Intento de imagen previa a reparación

El 24-09-2026 se intentó crear una imagen previa a reparación con `ntfsclone --save-image --force --full-logfile`.

Resultado:

```text
$MFTMirr does not match $MFT (record 3)
Opening NTFS failed: Input/output error
ntfsclone exit_code=1
```

No se ejecutó ninguna reparación sobre el NTFS. El fallo confirma que la inconsistencia de metadatos impide a `ntfsclone` abrir el volumen en modo normal. TD-021 permanece pausado.


## Intento de imagen de metadatos NTFS

El 24-09-2026 también se intentó extraer una imagen de metadatos con `ntfsclone --metadata --save-image --ignore-fs-check --force --full-logfile`.

Resultado:

```text
$MFTMirr does not match $MFT (record 3)
Opening NTFS failed: Input/output error
ntfsclone exit_code=1
```

No se realizaron escrituras ni reparaciones sobre el volumen. La inconsistencia impide a `ntfsclone` abrir el NTFS incluso en modo de metadatos.


## Incidente NTFS — resuelto

El 24-09-2026 el volumen externo `InfoDGRC` fue reparado mediante Windows Recovery ejecutado temporalmente en QEMU/KVM, sin instalar Windows y exponiendo únicamente el SSD externo.

Validaciones posteriores:

```text
chkdsk C: /f: sin problemas encontrados
fsutil dirty query C:: volumen sin errores
Debian: montaje normal mediante udisksctl
Filesystem: ntfs3
Modo: rw
UUID: A2B411E1B411B92D
Repositorio Restic: a1f88f2a
Snapshots: 0
restic check: no errors were found
```

El incidente queda cerrado. TD-021 puede continuar con la creación del primer snapshot certificado y su restauración real.


## PostgreSQL desde snapshot Restic — validado funcionalmente

Validado el 24-09-2026 usando el snapshot:

```text
Tag: SineOsBackups-240926-2334
Snapshot: 536d25fd
```

Cadena validada:

```text
PostgreSQL productivo
→ dump lógico
→ snapshot Restic
→ restore temporal
→ hashes SHA-256
→ PostgreSQL 18 temporal aislado
→ restore de globals.sql
→ restore de database.dump
→ validación de roles y estructura
```

Resultados:

```text
Roles no-sistema recuperados: 1
Tablas de usuario: 0
Secuencias de usuario: 0
Vistas de usuario: 0
Red del contenedor temporal: none
Puertos publicados: ninguno
Entorno temporal eliminado: OK
PostgreSQL productivo final: Running=false / ExitCode=0
Residuos temporales: ninguno
```

PostgreSQL queda funcionalmente recuperable desde el snapshot Restic. TD-021 continúa abierto hasta completar las validaciones funcionales restantes y el cierre documental/sincronización del backup.


## Uptime Kuma desde snapshot Restic — validado funcionalmente

Validado el 24-09-2026 usando el snapshot:

```text
Tag: SineOsBackups-240926-2334
Snapshot: 536d25fd
```

Cadena validada:

```text
Uptime Kuma productivo apagado limpio
→ snapshot Restic
→ restore temporal
→ copia de trabajo
→ contenedor aislado
→ recuperación MariaDB
→ respuesta HTTP
→ apagado limpio
→ destrucción del entorno temporal
```

Resultados:

```text
Archivos restaurados: 261
Tamaño restaurado: 180M
MariaDB/kuma presente: sí
NetworkMode: none
Puertos publicados: ninguno
Respuesta HTTP: 302
Estabilidad posterior: OK
Apagado temporal: ExitCode=0
Restore original sin modificar: OK
Copia de trabajo eliminada: OK
Uptime Kuma productivo final: Running=false / ExitCode=0
Residuos temporales: ninguno
```

Uptime Kuma queda funcionalmente recuperable desde el snapshot Restic. TD-021 continúa abierto hasta completar las validaciones restantes y el cierre documental/sincronización del respaldo.


## Open WebUI desde snapshot Restic — validado funcionalmente

Validado el 24-09-2026 usando el snapshot:

```text
Tag: SineOsBackups-240926-2334
Snapshot: 536d25fd
```

Cadena validada:

```text
Open WebUI productivo apagado limpio
→ snapshot Restic
→ restore temporal
→ copia de trabajo
→ validación SQLite
→ contenedor aislado
→ respuesta HTTP
→ apagado limpio
→ destrucción del entorno temporal
```

Resultados:

```text
SQLite webui.db: integrity_check OK
Tablas detectadas: 43
Cache excluida: sí
Contenedor temporal aislado: sí
Puertos publicados: ninguno
Respuesta HTTP: OK
Apagado temporal: ExitCode=0
Restore original sin modificar: OK
Copia de trabajo eliminada: OK
Open WebUI productivo final: Running=false / ExitCode=0
Residuos temporales: ninguno
```

Open WebUI queda funcionalmente recuperable desde el snapshot Restic. TD-021 continúa abierto hasta completar Stirling PDF y el cierre documental/sincronización del respaldo.


## Stirling PDF desde snapshot Restic — validado funcionalmente

Validado el 24-09-2026 usando el snapshot:

```text
Tag: SineOsBackups-240926-2334
Snapshot: 536d25fd
```

Cadena validada:

```text
Stirling PDF productivo apagado limpio
→ snapshot Restic
→ restore temporal
→ copia de trabajo
→ contenedor aislado
→ respuesta HTTP
→ validación de base MV
→ apagado limpio
→ destrucción del entorno temporal
```

Resultados:

```text
Archivos restaurados: 10
Tamaño restaurado: 160K
Base MV restaurada: presente
Imagen: docker.stirlingpdf.com/stirlingtools/stirling-pdf:2.14.3-fat
NetworkMode: none
Puertos publicados: ninguno
Respuesta HTTP: 200
Estabilidad posterior: OK
Apagado temporal: ExitCode=0
Restore original sin modificar: OK
Copia de trabajo eliminada: OK
Stirling PDF productivo final: Running=false / ExitCode=0
Residuos temporales: ninguno
```

Stirling PDF queda funcionalmente recuperable desde el snapshot Restic. Con PostgreSQL, Uptime Kuma, Open WebUI, Stirling PDF y el Knowledge Vault ya restaurados y validados, TD-021 queda listo para su cierre documental y sincronización final.
